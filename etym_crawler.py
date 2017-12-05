import re
import os
import requests
import html
import json
import random
import time

finder = re.compile(r'<div class=\"word--C9UPa\">.*?<object>(.*?)</object>.*?</div>', re.DOTALL)

def __crawl_single_word(word):
  url = r"https://www.etymonline.com/word/{}".format(word)
  response = requests.get(url)
  t = response.text
  results = finder.findall(t)
  return [html.unescape(line).replace('<p>', '').replace('</p>', '') for line in results]

def crawl_list(word_list):
  d = {}
  for w in word_list:
    print("crawling", w, "...", end="")
    if os.path.exists("etymonline/"+w+".txt"):
      print("already exists")
      continue
    r = __crawl_single_word(w)
    d[w] = r
    j = {w: r}
    with open("etymonline/"+w+".txt", "w", encoding="utf-8") as fout:
      fout.write(json.dumps(j))
    print("done")
    time.sleep(random.randrange(1, 2))
  return d