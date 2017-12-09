# find:
# <meta property="og:title" content="English Dictionary, Thesaurus, &amp; grammar help | Oxford Dictionaries" />


import os
import re
import json
import time
import pandas as pd

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
                         deriv_r, origin_r, result_r,
                         oxford_dir="oxford"):
  fpath = os.path.join(oxford_dir, word + ".html")
  if not os.path.exists(fpath):
    return "file not exists!", -9
  with open(fpath, "r", encoding='utf-8') as fin:
    t = fin.read()
  if deriv_r.search(t):
    return deriv_r.findall(t)[0], 1
  elif origin_r.search(t):
    return origin_r.findall(t)[0], 2
  elif result_r.search(t):
    title = result_r.findall(t)[0]
    if re.match(word, title):
      return "other", 0
    else:
      return "not a word", -1
  else:
    return "unknown", -999
    
def divide_deriv_origin_other_no(wordlist, oxford_dir="oxford",
                                 deriv_rule=r'<p class="derivative_of">See <a href="(.*?)">\1</a></p>',
                                 origin_rule=r'<section class="etymology etym"><h3><strong>Origin</strong></h3><div class="senseInnerWrapper"><p>(.*?)</p></div></section>',
                                 result_rule=r'<meta property="og:title" content="([^/<>]*?)" />'):
  
  d = {}
  deriv_r = re.compile(deriv_rule)
  origin_r = re.compile(origin_rule)
  result_r = re.compile(result_rule)
  for word in wordlist:
    d[word], _ = __divide_single_word(word, oxford_dir=oxford_dir, deriv_r=deriv_r, origin_r=origin_r, result_r=result_r)
  return d


def divide_deriv_origin_other_no_to_csv(wordlist, oxford_dir="oxford",
                                 deriv_rule=r'<p class="derivative_of">See <a href="(.*?)">\1</a></p>',
                                 origin_rule=r'<section class="etymology etym"><h3><strong>Origin</strong></h3><div class="senseInnerWrapper"><p>(.*?)</p></div></section>',
                                 result_rule=r'<meta property="og:title" content="([^/<>]*?)" />'):
  deriv_r = re.compile(deriv_rule)
  origin_r = re.compile(origin_rule)
  result_r = re.compile(result_rule)
  data = []
  cnt = 0
  code_dict = {}
  t0 = time.time()
  for word in wordlist:
    detail, code = __divide_single_word(word, oxford_dir=oxford_dir, deriv_r=deriv_r, origin_r=origin_r, result_r=result_r)
    data.append([word, detail, code])
    if code in code_dict:
      code_dict[code] += 1
    else:
      code_dict[code] = 1
    cnt += 1
    if cnt % 100 == 0:
      delta_t = time.time() - t0
      print(cnt, code_dict, delta_t*(13200-cnt)/cnt/60)
      t0 = time.time()

  df = pd.DataFrame(data, columns=['word', 'detail', 'code'])
  df.to_csv("oxford_divide_new/oxford_full_1209.csv", encoding="utf-8")

  # code: 1(deriv), 2(origin), 0(other), -1(naw), -9(fne), -999(unknwon)
  for code in [1,2,0,-1,-9,-999]:
    temp_df = df[df.code==code]
    temp_df.to_csv("oxford_divide_new/code_{}.csv".format(code), encoding="utf-8")
  
  with open("oxford_divide_new/to_wordsapi.txt", "w", encoding="utf-8") as fout:
    for w in df[df.code==2].word:
      fout.write(w+'\n')
    for w in df[df.code==0].word:
      fout.write(w+'\n')

  return df


if __name__ == "__main__":
  '''
  print("start")
  og_title_tag_from_html()
  print("end")
  '''
  with open("to_crawl_all_words.txt", "r", encoding='utf-8') as fin:
    wl = fin.read().split('\n')
  df = divide_deriv_origin_other_no_to_csv(wl)
  print("done")
  
