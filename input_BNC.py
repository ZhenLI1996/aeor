import os
import json
import xml
from nltk.corpus.reader.bnc import BNCCorpusReader as bnc_reader
import re
import time

DIR_BNC_ROOT = "../../../corpora/BNC-XML/Texts"

PATH_BNC_G1H = "../../../corpora/BNC-XML/Texts/G/G1/G1H.xml"

TEST_TARGET_FILEIDS = ["G/G1/G1H.xml"]

print("creating global bnc reader")
global_bnc = bnc_reader(root=DIR_BNC_ROOT, fileids=r'[A-K]/\w*/\w*\.xml')
global_word_rule = re.compile(r'\w+?[aeo]rs?$')
global_tag_rule = re.compile(r'(?:.*?-)*?NN[012](?:-.*?)*?')


def __by_fileidlist(bnc=global_bnc,  word_rule=global_word_rule, tag_rule=global_tag_rule, fileidlist=TEST_TARGET_FILEIDS, visible=True):
  #tag_rule = re.compile(r'NN[012]')
  d = {}
  length = len(fileidlist)
  words_c5 = bnc.tagged_words(fileids=fileidlist, c5=True)
  if visible:
    print("filtering... ", end='', flush=True)
  f = filter(lambda i: tag_rule.match(i[1]), filter(lambda i: word_rule.match(i[0]), words_c5))
  if visible:
    print("updating dict... ", end='', flush=True)
  for w, t in f:
    w = w.lower()
    if re.search(r'[^A-Za-z]', w):
      continue  # not A-Za-z occurs
    if w[-1] == 's':
      w = w[:-1]
    if w not in d:
      d[w] = [t]
    elif t not in d[w]:
      d[w].append(t)
  return d

def read(bnc_root=DIR_BNC_ROOT, visible=True, output_path="BNC_word_c5_NNonly.txt"):
  t_start = time.time()
  t0 = t_start
  d = {}
  cnt = 1
  def __update(x, y=d):
    if x[0] not in y:
      y[x[0]] = x[1]
    else:
      for i in x[1]:
        if i not in y[x[0]]:
          y[x[0]].append(i)
  for root, dirs, files in os.walk(bnc_root):
    for d1 in dirs:
      for root, dirs, files in os.walk(bnc_root + '/' + d1):
        for d2 in dirs:
          if visible:
            print("in \"{}\" ...".format(bnc_root + '/' + d1 + '/' + d2))
          cur_list = []
          for root, dirs, files in os.walk(bnc_root + '/' + d1 + '/' + d2):
            for file in files:
                cur_list.append(d1 + '/' + d2 + '/' + file)
          d_ = __by_fileidlist(fileidlist=cur_list)
          for i in map(__update, d_.items()):
            pass # run the map
          if visible:
            t1 = time.time()
            print("done. time used: {:.3f} secs".format(t1-t0))
            print("count: {}, average time comsumption:{:.3f} secs".format(cnt, (t1-t_start)/cnt))
            t0 = t1
            cnt += 1
  
  if visible:
    print("output to file")
  with open(output_path, "w", encoding="utf-8") as fout:
    fout.write(json.dumps(d))
  if visible:
    print("done")
  return d



# === depricated ===

def get_BNC_file_list(bnc_root=DIR_BNC_ROOT):
  file_list = []
  for root, dirs, files in os.walk(bnc_root):
    for d1 in dirs:
      for root, dirs, files in os.walk(bnc_root + '/' + d1):
        for d2 in dirs:
          for root, dirs, files in os.walk(bnc_root + '/' + d1 + '/' + d2):
            for file in files:
              file_list.append(d1 + '/' + d2 + '/' + file)
  return file_list

def read_BNC_visible(bnc_root=DIR_BNC_ROOT, target_fileids=TEST_TARGET_FILEIDS):
  
  d = {}
  r = re.compile(r'\w+?[aeo]rs?$')
  bnc = global_bnc
  print("reading words")
  length = len(target_fileids)
  t_start = time.time()
  t0 = t_start
  for fileid, i in zip(target_fileids, range(1, length+1)):
    print("{:4}/{:4} reading {}".format(i, length, fileid), end='', flush=True)
    c5_words = bnc.tagged_words(fileids=[fileid], c5=True)
    #print("filtering")
    #f = filter(r.match, words)
    #print("creating result set")
    #s = s | set(((w.lower(), c5) for w, c5 in f))
    for w, c5 in c5_words:
      w = w.lower()
      if w[-1] == 's':  # eliminate pural '-s'
        w = w[:-1]
      if not r.match(w):
        continue
      if w not in d:
        d[w] = [c5]
      elif c5 not in d[w]:
        d[w].append(c5)
    t1 = time.time()
    est = (t1 - t_start) * (length - i) / i
    print("\t\tc:{:.1f}, est:{}:{:.1f}".format(t1-t0, int(est/60), est%60))
    t0 = t1

  print("writing file")
  with open("BNC_raw_dict.txt", "w", encoding="utf-8") as fout:
    fout.write(json.dumps(d))
  print("writing successfully")
  return d


def read_BNC_visible_NNonly(bnc_root=DIR_BNC_ROOT, target_fileids=TEST_TARGET_FILEIDS, output="BNC_raw_dict_NNonly.txt"):
  print("creating bnc reader")
  bnc = bnc_reader(root=bnc_root, fileids=r'[A-K]/\w*/\w*\.xml')
  
  d = {}
  r = re.compile(r'\w+?[aeo]rs?$')

  print("reading words")
  length = len(target_fileids)
  t_start = time.time()
  t0 = t_start
  for fileid, i in zip(target_fileids, range(1, length+1)):
    print("{:4}/{:4} reading {}".format(i, length, fileid), end='', flush=True)
    c5_words = bnc.tagged_words(fileids=[fileid], c5=True)
    #print("filtering")
    #f = filter(r.match, words)
    #print("creating result set")
    #s = s | set(((w.lower(), c5) for w, c5 in f))
    for w, c5 in c5_words:
      w = w.lower()
      if not re.match(r'NN[012]', c5):  # skip other pos
        continue
      if w[-1] == 's':  # eliminate pural '-s'
        w = w[:-1]
      if not r.match(w):
        continue
      if w not in d:
        d[w] = [c5]
      elif c5 not in d[w]:
        d[w].append(c5)
    t1 = time.time()
    est = (t1 - t_start) * (length - i) / i
    print("\t\tc:{:.1f}, est:{}:{:.1f}".format(t1-t0, int(est/60), est%60))
    t0 = t1

  print("writing file")
  with open(output, "w", encoding="utf-8") as fout:
    fout.write(json.dumps(d))
  print("writing successfully")
  return d

if __name__ == "__main__":
  read_BNC_visible(target_fileids=get_BNC_file_list())
  print("DONE!")