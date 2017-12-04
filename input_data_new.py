import os
import re
import string

import requests

import traceback
import datetime

print("input_data_new: importing NLTK")
import nltk
print("input_data_new: NLTK imported")

DIR_FLOB = '../../../corpora/FLoB_Frown_XML/FLoB_Frown_XML/FLOB_XML/FLOB'
PATH_FLOB_A = DIR_FLOB + '/flob_a.xml'

def __read_FLOB_file(path):
  # print instruction
  print("reading file: ", path)
  # read raw text, change into lower case
  with open(path, 'r', encoding='utf-8', errors='ignore') as fin:
    text = fin.read().lower()
  # find all raw words with regex
  raw_tags = re.findall(r'<w (?:pos|POS)="(?:nn|NN)1\w*?">\w+?(?:er|ar|or)</w>', text)
  #raw_words = re.findall(r'(?:<w pos="nn1\w*?">)(\w+?(?:er|ar|or))(?:</w>)', text)
  d = {}
  raw_tags = set(raw_tags)
  for t in raw_tags:
    w = re.findall(r'(?:<w pos="nn1\w*?">)(\w+?(?:er|ar|or))(?:</w>)', t)[0]
    d[w] = t
  # lemmatize
  #raw_toks = set((w.strip(string.punctuation) for w in raw_words))
  #toks = set((lemmatizer.lemmatize(w) for w in raw_toks))
  #return raw_toks, toks
  #tag_set = set(raw_tags)
  #word_set = set(raw_words)
  return d



def read_FLOB(dir=DIR_FLOB):
  d_all = {}
  for root, dirs, files in os.walk(dir):
    for file in files:
      d = __read_FLOB_file(dir + '/' + file)
      d_all.update(d)
  return d_all

'''
def __read_FLOB_file(path):
  # print instruction
  print("reading file: ", path)
  # read raw text, change into lower case
  with open(path, 'r', encoding='utf-8', errors='ignore') as fin:
    text = fin.read().lower()
  # find all raw words with regex
  raw_tags = re.findall(r'<w (?:pos|POS)="(?:nn|NN)1\w*?">\w+?(?:er|ar|or)</w>', text)
  raw_words = re.findall(r'(?:<w pos="nn1\w*?">)(\w+?(?:er|ar|or))(?:</w>)', text)
  # lemmatize
  #raw_toks = set((w.strip(string.punctuation) for w in raw_words))
  #toks = set((lemmatizer.lemmatize(w) for w in raw_toks))
  #return raw_toks, toks
  tag_set = set(raw_tags)
  word_set = set(raw_words)
  return tag_set, word_set



def read_FLOB(dir):
  all_eaor_tags = set()
  all_eaor_words = set()

  for root, dirs, files in os.walk(dir):
    for file in files:
      cur_tags, cur_words = __read_FLOB_file(dir + '/' + file)
      all_eaor_tags = all_eaor_tags | cur_tags
      all_eaor_words = all_eaor_words | cur_words
  return all_eaor_tags, all_eaor_words
'''


def __download_word(word):
  if os.path.exists('wordsapi/{}.txt'.format(word)):
    return "already exists"
  
  try:
    headers={
      "X-Mashape-Key": "cJEf2iokzbmshxtkkzKrYjxR2ANkp16Jv6Vjsn5cKyHkbdwBCK",
      "Accept": "application/json"
    }
    url = 'https://wordsapiv1.p.mashape.com/words/' + word
    r = requests.get(url, headers=headers)
    
    with open('wordsapi/{}.txt'.format(word), 'w', encoding='utf-8') as fout:
      fout.write(r.content.decode())
    return "download successfully"
  except Exception as e:
    return e


def download(word_list):
  length = len(word_list)
  log = "\n\n===" + str(datetime.datetime.now()) + "===\n\n"
  log_temp = "{word}: {state}\n"
  for i, w in zip(range(1, length+1), word_list):
    print("{:>4d}/{}: {}".format(i, length, w))
    ret = __download_word(w)
    log += log_temp.format(word=w, state=ret)
    print("\t" + str(ret))
  with open('download_log.txt', 'a', encoding='utf-8') as fout:
    fout.write(log)
  
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))