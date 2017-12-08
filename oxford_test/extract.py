# find:
# <meta property="og:title" content="English Dictionary, Thesaurus, &amp; grammar help | Oxford Dictionaries" />


import os
import re
import json
import time

DEFAULT_RULE = r'<meta property="og:title" content="([^/<>]*?)" />'

def extract_from_html(wordlist_path="to_crawl.txt", html_temp="oxford/{}.html", 
                      rule=DEFAULT_RULE,
                      output_path="extract_output.txt", output_flag=True):

  with open(wordlist_path, "r", encoding="utf-8") as fin:
    wl = fin.read().split('\n')

  d = {}
  r = re.compile(rule)

  length = len(wl)
  cnt = 0
  t0 = time.time()
  for w in wl:
    #print(w, end=' ', flush=True)
    html_path = html_temp.format(w)
    if not os.path.exists(html_path):
      #print("not exists!")
      d[w] = "not exists!"
    else:
      with open(html_path, "r", encoding="utf-8") as fin:
        html = fin.read()
      if not r.search(html):
        #print("og:title not found!")
        d[w] = "not found!"
      else:
        #print("extracted")
        d[w] = r.findall(html)[0]
    cnt += 1
    if cnt % 50 == 0:
      delta_t = (time.time() - t0) / cnt * (length - cnt)
      print(cnt, "/", length, "; estimated: {.1f}".format(delta_t))
  
  if output_flag:
    with open(output_path, "w", encoding="utf-8") as fout:
      fout.write(json.dumps(d))
  print("done")
  return d

if __name__ == "__main__":
  print("start")
  extract_from_html()
  print("end")
