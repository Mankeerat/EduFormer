from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

<<<<<<< HEAD
def generate_summary(rawdocs):
    print('Summarizing texts ...')
    stopwords = list(STOP_WORDS)
=======
import torch
from transformers import T5ForConditionalGeneration,T5Tokenizer
from nltk.tokenize import sent_tokenize
import random
import numpy as np
import nltk
nltk.download('punkt')

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

def generate_summary(text):
    model = T5ForConditionalGeneration.from_pretrained('t5-base')
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
>>>>>>> parent of ca072d0 (complete transcript part)

    nlp = spacy.load('en_core_web_trf')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1


    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)

    summary = nlargest(select_len, sent_scores, key = sent_scores.get)


    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(summary, doc)
    return summary
    #  ,doc, len(rawdocs.split(' ')), len(summary.split(' '))
    


