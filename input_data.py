import os
import re
import string

print("input_data: importing nltk")
import nltk

stemmer = nltk.stem.snowball.SnowballStemmer('english')
lemmatizer = nltk.stem.WordNetLemmatizer()



DIR_LOCNESS = '../../../corpora/LOCNESS/alevels_raw'
DIR_FLOB = '../../../corpora/FLoB_Frown_XML/FLoB_Frown_XML/FLOB_XML/FLOB'

def read_FLOB_file(path):
  # print instruction
  print("reading file: ", path)
  # read raw text, change into lower case
  with open(path, 'r', encoding='utf-8', errors='ignore') as fin:
    text = fin.read().lower()
  # find all raw words with regex
  raw_words = re.findall(r'<w.*?>(.*?)</w>', text)
  # lemmatize
  raw_toks = set((w.strip(string.punctuation) for w in raw_words))
  toks = set((lemmatizer.lemmatize(w) for w in raw_toks))
  return raw_toks, toks


def read_FLOB(dir):
  all_raw_toks = set()
  all_toks = set()
  for root, dirs, files in os.walk(dir):
    for file in files:
      cur_raw_toks, cur_toks = read_FLOB_file(dir + '/' + file)
      all_raw_toks  = all_raw_toks  | cur_raw_toks
      all_toks = all_toks | cur_toks
  return all_raw_toks, all_toks


# === LOCNESS ===============

def read_file_raw(path):
  # print instruction
  print("reading file: ", path)
  # read raw text, change into lower case
  with open(path, 'r', encoding='utf-8', errors='ignore') as fin:
    text = fin.read().lower()
  # find the set of all hyphenated words (h_w: hyphen_words)
  hws = set(re.findall(r'\w+(?:-\w+)+', text))
  # get token set
  #toks = set((stemmer.stem(w) for w in set(nltk.word_tokenize(text))))
  toks = set(nltk.word_tokenize(text))
  # return hyphenated words and
  return toks, hws

def read_raw(dir):
  
  all_toks = set()
  all_hws = set()
  
  for root, dirs, files in os.walk(dir):
    for file in files:
      cur_toks, cur_hws = read_file_raw(dir + '/' + file)
      all_toks = all_toks | cur_toks
      all_hws  = all_hws  | cur_hws
  
  return all_toks, all_hws

