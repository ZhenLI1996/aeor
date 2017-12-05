import os
import json
import traceback
import re

WORDSAPI_PATH = "./wordsapi"
DERIV_OUTPUT = "./divide3_output/deriv.txt"
OTHER_OUTPUT = "./divide3_output/other.txt"
NO_RES_OUTPUT = "./divide3_output/no_res.txt"

def divide3(wordlist):
  word_deriv = {}
  word_other = {}
  word_no_res = {}
  
  '''
  for root, dirs, files in os.walk(path):
    for file in files:
      word = re.findall(r'(.*?)\.txt', file)[0]
      file_dir = path + '/' + file
      with open(file_dir, 'r', encoding='utf-8') as fin:
        t = fin.read()
      j = json.loads(t)
   
      print(word)
      deriv = []
      if 'results' not in j:
        word_no_res[word] = ""
        continue
      
      for result in j['results']:
        if 'derivation' in result:
          deriv.append(result['derivation'])
      if len(deriv) == 0:
        # no derivations
        word_other[word] = ''
      else:
        word_deriv[word] = deriv
  '''
  for word in wordlist:
    #print(word)
    path = WORDSAPI_PATH + '/' + word + '.txt'
    if not os.path.exists(path):
      print("not exists!")
      continue
    
    with open(path, 'r', encoding='utf-8') as fin:
      t = fin.read()
    j = json.loads(t)
   
    deriv = []
    if 'results' not in j:
      print(word)
      word_no_res[word] = ""
      continue
    
    for result in j['results']:
      if 'derivation' in result:
        deriv.append(result['derivation'])
    if len(deriv) == 0:
      # no derivations
      word_other[word] = ''
    else:
      word_deriv[word] = deriv
  with open(DERIV_OUTPUT, "w", encoding="utf-8") as fout_deriv,\
       open(NO_RES_OUTPUT, "w", encoding="utf-8") as fout_no_res,\
       open(OTHER_OUTPUT, "w", encoding="utf-8") as fout_other:
          fout_deriv.write(json.dumps(word_deriv))
          fout_no_res.write(json.dumps(word_no_res))
          fout_other.write(json.dumps(word_other))
  return word_deriv, word_other, word_no_res


def unfold_deriv(path=DERIV_OUTPUT):
  with open(path, 'r', encoding='utf-8') as fin:
    d = json.loads(fin.read())
  for k, v in d.items():
    temp_list = []
    for derivs in v:
      for deriv in derivs:
        temp_list.append(deriv)
    d[k] = set(temp_list)
  return d

def find_true_deriv(unfolder=unfold_deriv):
  d = unfold_deriv()
  d_true = {}
  d_false = {}
  for k, d_set in d.items():
    flag = False
    temp_list = []
    for i in d_set:
      if len(i) < len(k):
        flag = True
        temp_list.append(i)
    if flag:
      d_true[k] = temp_list
    else:
      d_false[k] = {}
  
  return d_true, d_false



def __let_user_choose(roots):
  print("there are multiple roots, please choose one:")
  for i, r in zip(range(0, len(roots)), roots):
    print(i, ")\t\t", r)
  i = int(input("choose: "))
  while i >= len(roots):
    i = int(input("invalid input.\nchoose: "))
  return roots[i]


def find_root(d_true):
  d = {}
  for k, roots in d_true.items():
    if len(roots) == 1:
      d[k] = roots[0]
    else:
      d[k] = __let_user_choose(roots)
  return d


