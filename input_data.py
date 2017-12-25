import pandas as pd 
import json, os

def read_oxford_result():
  d = {}
  parse_code = {0: ["other"],
                1: ["deriv", "derivative_of"],
                2: ["etym", "origin"],
                -1: ["naw", "not a word"],
                -9: ["unknown"],
                -999:["unknown"]}
  for i in [0,1,2,-1,-9,-999]:
    df = pd.read_csv("oxford_divide_new/code_{}.csv".format(i), encoding="utf-8", index_col=0)
    d[i] = df
    for p in parse_code[i]:
      d[p] = df
  
  return d



'''
possible code-status:
  0   -   is word but nothing else
  11  -   oxford deriv
  12  -   wordsapi deriv
  2   -   have oxford origin
  -1  -   not a word
  -9  -   unknown error
'''


def choose_derivation(word, deriv):
  proper_d = set()
  for d in deriv:
    if len(d) >= len(word):
      continue
    else:
      proper_d.add(d)
  proper_d = list(proper_d)
  if len(proper_d) == 0:
    return 0, "no proper derivation"
  elif len(proper_d) == 1:
    return 12, proper_d[0]
  else:
    return let_user_choose(word, proper_d)

def let_user_choose(word, proper_d):
  print("there are multiple derivations for\"{}\", please choose one:".format(word))
  proper_d.insert(0, "no match")
  length = len(proper_d)
  for i, d in zip(range(length), proper_d):
    print(i, d)
  i = input("you choose: ")
  while not i.isnumeric() or int(i) >= length or int(i) < 0:
    i = input("wrong input; you choose:")
  i = int(i)
  if i == 0:
    return 0, "user choose no derivation"
  else:
    return 12, proper_d[i]

def wordsapi(word):
  filepath = "wordsapi/{}.txt".format(word)

  if not os.path.exists(filepath):
    return -9, "file not exists"

  with open(filepath, "r", encoding="utf-8") as fin:
    t = fin.read()
  j = json.loads(t)

  if 'results' not in j:
    return 0, "no results in wordsapi"
  
  deriv = set()
  for result in j['results']:
    if 'derivation' in result:
      deriv = deriv | set(result['derivation'])
  if len(deriv) == 0:
    # no derivations
    return 0, "no derivations in wordsapi"
  else:
    return choose_derivation(word, deriv)

def divide_by_wordsapi(wordlist):
  d = {}
  for w in wordlist:
    d[w] = wordsapi(w)
  return d

# ===

'''
possible code-status:
  0   -   is word but nothing else
  11  -   oxford deriv
  12  -   wordsapi deriv
  2   -   have oxford origin
  -1  -   not a word
  -9  -   unknown error
'''

def main():
  l = []
  d = read_oxford_result()
  
  # === in oxford: ===
  df0 = d[0]
  df1 = d[1]
  df2 = d[2]
  # === end oxford ===
  print("start")
  cnt = 0
  length = len(df1)
  for index, row in df1.iterrows():
    l.append([row['word'], row['detail'], 11])
    cnt += 1
    if cnt % 20 == 0:
      print("df1:{}/{}".format(cnt, length))
  cnt = 0
  length = len(df2)
  for index, row in df2.iterrows():
    w = row['word']
    code, detail = wordsapi(w)
    if code == 0:
      l.append([w, row['detail'], 2])
    else:
      l.append([w, detail, code])
    cnt += 1
    if cnt % 20 == 0:
      print("df2:{}/{}".format(cnt, length))
  cnt = 0
  length = len(df0)
  for index, row in df0.iterrows():
    w = row['word']
    code, detail = wordsapi(w)
    l.append([w, detail, code])
    cnt += 1
    if cnt % 20 == 0:
      print("df0:{}/{}".format(cnt, length))
  print("creating dataframe")
  df = pd.DataFrame(l, columns=['word', 'detail', 'code'])
  print("write to file")
  df.index += 1
  df.to_csv("oxford_wordsapi_divide.csv", encoding='utf-8')
  print("done")
  return df