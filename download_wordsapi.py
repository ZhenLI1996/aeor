import os

import requests

import datetime

def __download_word(word):
  if os.path.exists('wordsapi/{}.txt'.format(word)):
    return "already exists"
  
  try:
    headers = {
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
  with open('diff_downloaded.txt', 'a', encoding='utf-8') as fout:
    for i, w in zip(range(1, length + 1), word_list):
      fout.write(w + '\n')
      print("{:>4d}/{}: {}".format(i, length, w))
      ret = __download_word(w)
      log += log_temp.format(word=w, state=ret)
      print("\t" + str(ret))
  with open('download_log.txt', 'a', encoding='utf-8') as fout:
    fout.write(log)
    
def download_other_1208():
  with open("to_wordsapi.txt", "r", encoding="utf-8") as fin:
    t = fin.read()
  list_o = set(t.split('\n'))
  with open('diff_downloaded.txt', 'r', encoding='utf-8') as fin:
    diff_downloaded = fin.read().split('\n')
  i = 0
  cnt = 0
  targets = list(set(list_o) - set(diff_downloaded))

  log = "\n\n===" + str(datetime.datetime.now()) + "===\n\n"
  log_temp = "{word}: {state}\n"
  with open('diff_downloaded.txt', 'a', encoding='utf-8') as fout:
    while cnt < 2450 and i < len(targets):
      w = targets[i]
      fout.write(w + '\n')
      print(cnt, w)
      ret = __download_word(w)
      log += log_temp.format(word=w, state=ret)
      print("\t" + str(ret))
      if ret == "download successfully":
        cnt += 1
      i += 1
    
  with open('download_log.txt', 'a', encoding='utf-8') as fout:
    fout.write(log)
    
def download_other_1210():
  with open("to_wordsapi_1210.txt", "r", encoding="utf-8") as fin:
    t = fin.read()
  targets = t.split('\n')

  log = "\n\n===" + str(datetime.datetime.now()) + "===\n\n"
  log_temp = "{word}: {state}\n"
  i = 0
  cnt = 0
  while cnt < 2450 and i < len(targets):
    w = targets[i]
    print(cnt, w)
    ret = __download_word(w)
    log += log_temp.format(word=w, state=ret)
    print("\t" + str(ret))
    if ret == "download successfully":
      cnt += 1
    i += 1
    
  with open('download_log.txt', 'a', encoding='utf-8') as fout:
    fout.write(log)
    
  

if __name__ == "__main__":
  '''
  with open('diff.txt', 'r', encoding='utf-8') as fin:
    diff = fin.read().split('\n')
  with open('diff_downloaded.txt', 'r', encoding='utf-8') as fin:
    diff_downloaded = fin.read().split('\n')
  remain = list(set(diff) - set(diff_downloaded))
  if len(remain) < 2450:
    download(remain)
  else:
    download(remain[:2450])
  '''
  download_other_1210()
