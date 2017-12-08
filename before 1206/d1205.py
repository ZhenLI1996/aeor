import json

import etym_crawler


with open('divide3_output/other.txt', 'r', encoding='utf-8') as fin:
  j = json.loads(fin.read())

l = list(j.keys())

etym_crawler.crawl_list(l)

print("DONE!")
