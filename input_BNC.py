import os
import json
import xml
from nltk.corpus.reader.bnc import BNCCorpusReader as bnc_reader
import re
import time

DIR_BNC_ROOT = "../../../corpora/BNC-XML/Texts"

PATH_BNC_G1H = "../../../corpora/BNC-XML/Texts/G/G1/G1H.xml"

TEST_TARGET_FILEIDS = ["G/G1/G1H.xml"]

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
  print("creating bnc reader")
  bnc = bnc_reader(root=bnc_root, fileids=r'[A-K]/\w*/\w*\.xml')
  
  d = {}
  r = re.compile(r'\w+?[aeo]r$')

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


if __name__ == "__main__":
  read_BNC_visible(target_fileids=get_BNC_file_list())
  print("DONE!")