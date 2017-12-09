import requests
import os

import threading
import time
import json

import random

URL_TEMP = 'https://en.oxforddictionaries.com/definition/{word}'

LOG_PATH_TEMP = 'download_{id}.log'

def download_word(word):
  file_path = 'oxford/{word}.html'.format(word=word)
  url = URL_TEMP.format(word=word)
  if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as fin:
      t = fin.read()
    if t == 'Retry later\n' or len(t) < 20:
      os.remove(file_path)
      log = word + " blocked"
      return -2, log
    else:
      log = word + " already exists!"
      #print(log)
      #with open(LOG_PATH, "a", encoding="utf-8") as fout:
        #fout.write(log + '\n')
      return 1, log
  else:
    try:
      response = requests.get(url)
      if response.text == 'Retry later\n' or len(response.text) < 20:
        log = word + " blocked"
        return -2, log
      with open(file_path, "w", encoding="utf-8") as fout:
        fout.write(response.text)
      log = word + " downloaded successfully"
      #print(log)
      #with open(LOG_PATH, "a", encoding="utf-8") as fout:
        #fout.write(log + '\n')
      return 0, log
    except Exception as e:
      log = word + " other exception: " + str(e)
      #print(log)
      #with open(LOG_PATH, "a", encoding="utf-8") as fout:
        #fout.write(log + '\n')
      return -1, log


class MyThread(threading.Thread):
  def __init__(self, threadID, wordlist):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.wordlist = wordlist
  def run(self):
    block_cnt = 0
    print("start thread", self.threadID)
    length = len(self.wordlist)
    
    whole_log = ''
    code_list = []
    d = {0:0, 1:0, -1:0, -2:0}
    i = 0
    t0 = time.time()
    suc_cnt = 0
    for w in self.wordlist:
      i += 1
      code, log = download_word(w)
      if code == -2:
        # blocked
        block_cnt += 1
        print("id:{}, {:2}/{:2}".format(self.threadID, i, length), w, "blocked, retry later")
        self.wordlist.insert(0, w)
        i -= 1        
      elif code < 0:
        # error
        print("id:{}, {:2}/{:2}".format(self.threadID, i, length), w, "error occurred, retry later")
        self.wordlist.append(w)
        i -= 1
      elif code == 0:
        block_cnt = 0
        suc_cnt += 1
        print("id:{}, {:2}/{:2}".format(self.threadID, i, length), w, "successfully downloaded in this request")
        print("suc_cnt/tot_time = {}/{:.3f}".format(suc_cnt, (time.time() - t0)*35/max(1, suc_cnt)))
      elif code == 1:
        #block_cnt = 0
        #print(w, "already exists")
        pass
      code_list.append(code)
      whole_log += log + '\n'
      if block_cnt >= 5:
        # wait 
        to_wait = min(2**(block_cnt-5), 60) * 60
        print("error too much, waiting", to_wait)
        time.sleep(to_wait)
      
      
    for c in code_list:
      d[c] += 1
    with open(LOG_PATH_TEMP.format(id=self.threadID), "w", encoding="utf-8") as fout:
      fout.write(whole_log + '\n')
      fout.write(json.dumps(d))
      
    print("end thread:", self.threadID, d)
    
def multi_thread(thread_num=10):
  spider_num = thread_num
  with open("to_crawl_all_words.txt", "r", encoding="utf-8") as fin:
    wl = fin.read().split('\n')
  random.shuffle(wl)
  gap = int(len(wl) / spider_num) + 1
  threads = []
  for i in range(spider_num):
    t = MyThread(i, wl[i*gap: i*gap+gap])
    threads.append(t)
  for t in threads:
    t.start()    
  for t in threads:
    t.join()
  print("done!")


if __name__ == "__main__":
  multi_thread(2)
