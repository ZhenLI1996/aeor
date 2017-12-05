import os
import json
import xml
from nltk.corpus.reader.bnc import BNCCorpusReader as bnc_reader
import re

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
  
  s = set()
  r = re.compile(r'\w+?[aeo]r$')

  print("reading words")
  cnt = 0
  for fileid in target_fileids:
    print("reading ", fileid, "count: ", cnt)
    cnt += 1
    words = bnc.words(fileids=[fileid])
    #print("filtering")
    f = filter(r.match, words)
    #print("creating result set")
    s = s | set((w.lower() for w in f))

  print("writing file")
  with open("BNC_raw_words.txt", "w", encoding="utf-8") as fout:
    for w in s:
      fout.write(w)
      fout.write('\n')
  print("writing successfully")
  return s


if __name__ == "__main__":
  read_BNC_visible(target_fileids=get_BNC_file_list())
  print("DONE!")