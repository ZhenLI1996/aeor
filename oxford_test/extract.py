# find:
# <meta property="og:title" content="English Dictionary, Thesaurus, &amp; grammar help | Oxford Dictionaries" />


import os
import re
import json
import time

DEFAULT_RULE = r'<meta property="og:title" content="([^/<>]*?)" />'

def og_title_tag_from_html(wordlist_path="to_crawl.txt", html_temp="oxford/{}.html",
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
      print(cnt, "/", length, "; estimated: {:.1f}".format(delta_t))
  
  if output_flag:
    with open(output_path, "w", encoding="utf-8") as fout:
      fout.write(json.dumps(d))
  print("done")
  return d



def match_title(d):
  r1 = []   # have result, "have_result == 1, r1"
  r0 = []
  for w, t in d.items():
    if re.match(w, t):
      r1.append(w)
    else:
      r0.append(w)
  return r1, r0

def find_derivative_of_or_origin(l, oxford_dir="oxford",
                                 deriv_rule=r'<p class="derivative_of">See <a href="(.*?)">\1</a></p>',
                                 origin_rule=r'<section class="etymology etym"><h3><strong>Origin</strong></h3><div class="senseInnerWrapper"><p>(.*?)</p></div></section>'):
  # <p class="derivative_of">See <a href="wisecrack">wisecrack</a></p>
  d = {}
  deriv_r = re.compile(deriv_rule)
  origin_r = re.compile(origin_rule)
  for w in l:
    fpath=os.path.join(oxford_dir, w+".html")
    if not os.path.exists(fpath):
      d[w] = "file not exists!"
      continue
    with open(fpath, "r", encoding='utf-8') as fin:
      t = fin.read()
    if deriv_r.search(t):
      d[w] = deriv_r.findall(t)[0]
    elif origin_r.search(t):
      d[w] = origin_r.findall(t)[0]
    else:
      d[w] = "no derivative_of"
  return d



def __divide_single_word(word,
                         oxford_dir="oxford",
                         deriv_rule=r'<p class="derivative_of">See <a href="(.*?)">\1</a></p>',
                         origin_rule=r'<section class="etymology etym"><h3><strong>Origin</strong></h3><div class="senseInnerWrapper"><p>(.*?)</p></div></section>',
                         result_rule=r'<meta property="og:title" content="([^/<>]*?)" />'):
  fpath = os.path.join(oxford_dir, word + ".html")
  deriv_r = re.compile(deriv_rule)
  origin_r = re.compile(origin_rule)
  result_r = re.compile(result_rule)
  if not os.path.exists(fpath):
    return "file not exists!"


  with open(fpath, "r", encoding='utf-8') as fin:
    t = fin.read()
  if deriv_r.search(t):
    return deriv_r.findall(t)[0]
  elif origin_r.search(t):
    return origin_r.findall(t)[0]
  elif result_r.search(t):
    return "other"
  else:
    return "not a word"
def divide_deriv_origin_other_no(wordlist, oxford_dir="oxford",
                                 deriv_rule=r'<p class="derivative_of">See <a href="(.*?)">\1</a></p>',
                                 origin_rule=r'<section class="etymology etym"><h3><strong>Origin</strong></h3><div class="senseInnerWrapper"><p>(.*?)</p></div></section>'):
  
  d = {}
  for word in wordlist:
    d[word] = __divide_single_word(word, oxford_dir=oxford_dir, deriv_rule=deriv_rule, origin_rule=origin_rule)
    
  return d





















if __name__ == "__main__":
  '''
  print("start")
  og_title_tag_from_html()
  print("end")
  '''
  with open("to_crawl_all_words.txt", "r", encoding='utf-8') as fin:
    wl = fin.read().split('\n')
  d = divide_deriv_origin_other_no(wl)
  print(d)
