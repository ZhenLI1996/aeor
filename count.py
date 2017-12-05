import json

def __get_test_words():
  with open("out_test1204_json.txt", "r", encoding="utf-8") as fin:
    j = json.loads(fin.read())
  return j


def __let_user_choose(word, temp):

  print("word: ", word)
  print("there are multiple pos, please choose one:")
  for i, r in zip(range(0, len(temp)), temp):
    print(i, ")\t\t", r)
  i = int(input("choose: "))
  while i >= len(temp):
    i = int(input("invalid input.\nchoose: "))
  return temp[i]

def get_pos_test(words=__get_test_words()):
  d = {}
  cnt = {"simple": 0, "complex": 0, "other": 0}
  for k, v in words.items():
    with open("./wordsapi/{}.txt".format(v), "r", encoding="utf-8") as fin:
      j = json.loads(fin.read())
      if 'results' in j:
        results = j['results']
        if len(results) == 1:
          r = results[0]
          if "partOfSpeech" in r:
            d[k] = {"word": v, "pos": r["partOfSpeech"]}
            cnt["simple"] += 1
          else:
            d[k] = {"word": v, "pos": ""}
            cnt["other"] += 1
        else:
          temp_set = set()
          for r in results:
            if "partOfSpeech" in r:
              temp_set.add(r["partOfSpeech"])
          if len(temp_set) == 1:
            d[k] = {"word": v, "pos": list(temp_set)[0]}
            cnt["simple"] += 1
          else:
            #d[k] = {"word": v, "pos": __let_user_choose(v, temp=temp_set)}
            d[k] = {"word": v, "pos": ""}
            cnt["complex"] += 1
      else:
        d[k] = {"word": v, "pos": ""}
        cnt["other"] += 1
  return d, cnt