# # -*- coding: utf-8 -*-
# """summary_to_quest.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/15VeXDaq833VeDdPM9ufCeesMyWvdFIbj
# """

import torch
from transformers import T5ForConditionalGeneration,T5Tokenizer
from collections import OrderedDict
from sklearn.metrics.pairwise import cosine_similarity
import random
import numpy as np
import string
import pke
import traceback
from sense2vec import Sense2Vec
import gradio as gr
from flashtext import KeywordProcessor
from sentence_transformers import SentenceTransformer
from similarity.normalized_levenshtein import NormalizedLevenshtein

import nltk
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# !wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
# !tar -xvf  s2v_reddit_2015_md.tar.gz

summary_model = T5ForConditionalGeneration.from_pretrained('t5-base')
summary_tokenizer = T5Tokenizer.from_pretrained('t5-base')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
summary_model = summary_model.to(device)

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_seed(42)

def postprocesstext (content):
  final=""
  for sent in sent_tokenize(content):
    sent = sent.capitalize()
    final = final +" "+sent
  return final

def summarizer(text,model,tokenizer):
  text = text.strip().replace("\n"," ")
  text = "summarize: "+text
  max_len = 512
  encoding = tokenizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt").to(device)

  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = model.generate(input_ids=input_ids,
                attention_mask=attention_mask,
                early_stopping=True,
                num_beams=3,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                min_length = 75,
                max_length=300
            )
  dec = [tokenizer.decode(ids,skip_special_tokens=True) for ids in outs]
  summary = dec[0]
  summary = postprocesstext(summary)
  summary= summary.strip()

  return summary

def get_nouns_multipartite(content):
    out=[]
    try:
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=content,language='en')
        pos = {'PROPN','NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
        keyphrases = extractor.get_n_best(n=15)
        
        for val in keyphrases:
            out.append(val[0])
    except:
        out = []
        traceback.print_exc()

    return out


def get_keywords(originaltext,summarytext):
  keywords = get_nouns_multipartite(originaltext)
  keyword_processor = KeywordProcessor()
  for keyword in keywords:
    keyword_processor.add_keyword(keyword)

  keywords_found = keyword_processor.extract_keywords(summarytext)
  keywords_found = list(set(keywords_found))

  important_keywords =[]
  for keyword in keywords:
    if keyword in keywords_found:
      important_keywords.append(keyword)

  return important_keywords[:4]

question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
question_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')
question_model = question_model.to(device)

def get_question(context,answer,model,tokenizer):
  text = "context: {} answer: {}".format(context,answer)
  encoding = tokenizer.encode_plus(text,max_length=384, pad_to_max_length=False,truncation=True, return_tensors="pt").to(device)
  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = model.generate(input_ids=input_ids,
                                  attention_mask=attention_mask,
                                  early_stopping=True,
                                  num_beams=5,
                                  num_return_sequences=1,
                                  no_repeat_ngram_size=2,
                                  max_length=72)


  dec = [tokenizer.decode(ids,skip_special_tokens=True) for ids in outs]

  Question = dec[0].replace("question:","")
  Question= Question.strip()
  return Question

s2v = Sense2Vec().from_disk('s2v_old')
sentence_transformer_model = SentenceTransformer('msmarco-distilbert-base-v3')

normalized_levenshtein = NormalizedLevenshtein()

def filter_same_sense_words(original,wordlist):
  filtered_words=[]
  base_sense =original.split('|')[1] 
  print (base_sense)
  for eachword in wordlist:
    if eachword[0].split('|')[1] == base_sense:
      filtered_words.append(eachword[0].split('|')[0].replace("_", " ").title().strip())
  return filtered_words

def get_highest_similarity_score(wordlist,wrd):
  score=[]
  for each in wordlist:
    score.append(normalized_levenshtein.similarity(each.lower(),wrd.lower()))
  return max(score)

def sense2vec_get_words(word,s2v,topn,question):
    output = []
    try:
      sense = s2v.get_best_sense(word, senses= ["NOUN", "PERSON","PRODUCT","LOC","ORG","EVENT","NORP","WORK OF ART","FAC","GPE","NUM","FACILITY"])
      most_similar = s2v.most_similar(sense, n=topn)
      output = filter_same_sense_words(sense,most_similar)
    except:
      output =[]

    threshold = 0.6
    final=[word]
    checklist =question.split()
    for x in output:
      if get_highest_similarity_score(final,x)<threshold and x not in final and x not in checklist:
        final.append(x)
    
    return final[1:]

def mmr(doc_embedding, word_embeddings, words, top_n, lambda_param):
    word_doc_similarity = cosine_similarity(word_embeddings, doc_embedding)
    word_similarity = cosine_similarity(word_embeddings)
    keywords_idx = [np.argmax(word_doc_similarity)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        candidate_similarities = word_doc_similarity[candidates_idx, :]
        target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)
        mmr = (lambda_param) * candidate_similarities - (1-lambda_param) * target_similarities.reshape(-1, 1)
        mmr_idx = candidates_idx[np.argmax(mmr)]
        keywords_idx.append(mmr_idx)
        candidates_idx.remove(mmr_idx)

    return [words[idx] for idx in keywords_idx]



def get_distractors_wordnet(word):
    distractors=[]
    try:
      syn = wn.synsets(word,'n')[0]
      
      word= word.lower()
      orig_word = word
      if len(word.split())>0:
          word = word.replace(" ","_")
      hypernym = syn.hypernyms()
      if len(hypernym) == 0: 
            return distractors
      for item in hypernym[0].hyponyms():
          name = item.lemmas()[0].name()
          if name == orig_word:
              continue
          name = name.replace("_"," ")
          name = " ".join(w.capitalize() for w in name.split())
          if name is not None and name not in distractors:
              distractors.append(name)
    except:
      print ("Wordnet distractors not found")

def get_distractors (word,origsentence,sense2vecmodel,sentencemodel,top_n,lambdaval):
  distractors = sense2vec_get_words(word,sense2vecmodel,top_n,origsentence)
  if len(distractors) ==0:
    return distractors
  distractors_new = [word.capitalize()]
  distractors_new.extend(distractors)

  embedding_sentence = origsentence+ " "+word.capitalize()
  keyword_embedding = sentencemodel.encode([embedding_sentence])
  distractor_embeddings = sentencemodel.encode(distractors_new)
  max_keywords = min(len(distractors_new),5)
  filtered_keywords = mmr(keyword_embedding, distractor_embeddings,distractors_new,max_keywords,lambdaval)
  final = [word.capitalize()]
  for wrd in filtered_keywords:
    if wrd.lower() !=word.lower():
      final.append(wrd.capitalize())
  final = final[1:]
  return final


def generate_summary_questions(context, modelopt):
    print('Generating summary...')
    summary_text = summarizer(context,summary_model,summary_tokenizer)
    print('Generating questions...')
    np =  get_keywords(context,summary_text)
    output = []
    for answer in np:
        temp = []
        ques = get_question(summary_text,answer,question_model,question_tokenizer)
        if modelopt=="Wordnet":
            distractors = get_distractors_wordnet(answer)
        else:
            distractors = get_distractors(answer.capitalize(),ques,s2v,sentence_transformer_model,40,0.2)
        temp = [ques, answer]
        if distractors and len(distractors)>0:
            for distractor in distractors[:4]:
                temp.append(distractor)
        output.append(temp)
    return output, summary_text