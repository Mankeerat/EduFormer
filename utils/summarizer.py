# def generate_summary(
#     # text
# ):
#     summary = "demo summary"
#     return summary

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

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    text = text.strip().replace("\n"," ")
    text = "summarize: "+text
    max_len = 512
    encoding = tokenizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt").to(device)

    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    outs = model.generate(
            input_ids=input_ids,
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
