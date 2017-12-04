import json

def __get_test_words():
  with open("out_test1204_json.txt", "r", encoding="utf-8") as fin:
    j = json.loads(fin.read())
  return j


def __let_user_choose(word, results):
  
  temp = set()
  for r in results:
    if "partOfSpeech" in r:
      temp.add(r["partOfSpeech"])
  
  temp = list(temp)
  if len(temp) == 1:
    return temp[0]
  else:
    print("word: ", word)
    print("there are multiple pos, please choose one:")
    for i, r in zip(range(0, len(temp)), temp):
      print(i, ")\t\t", r)
    i = int(input("choose: "))
    while i >= len(results):
      i = int(input("invalid input.\nchoose: "))
    return temp[i]

def get_pos(words=__get_test_words()):
  d = {}
  for k, v in words.items():
    with open("./wordsapi/{}.txt".format(v), "r", encoding="utf-8") as fin:
      j = json.loads(fin.read())
      if 'results' in j:
        results = j['results']
        if len(results) == 1:
          r = results[0]
          if "partOfSpeech" in r:
            d[k] = {"word": v, "pos": r["partOfSpeech"]}
          else:
            d[k] = {"word": v, "pos": ""}
        else:
          d[k] = {"word": v, "pos": __let_user_choose(v, results=results)}
      else:
        d[k] = {"word": v, "pos": ""}
  return d