# 工作流：
1.  提取出所有 -[aeo]r的词汇（称作*目标词*）: 
    - FLOB  *done*, "FLOB_raw_dict.txt"
    - BNC   *done*, "BNC_raw_words_ordered.txt"
2.  去`wordsapi`上把所有*目标词*的record都爬取下来：
    - FLOB  *done*, "wordsapi/xxx.txt"
    - BNC   *ing* , "wordsapi/xxx.txt"
3.  查找这个词的*基词*：
    3.1 用`filter.divide3`找到所有`wordsapi`里面有"derivation"的；然后用`filter.find_true_deriv`找到符合要求的deriv（暂定比*目标词*短的deriv；最后用`filter.find_root`找到真实的基词
    3.2 `filter.divide3`剩下来的部分，`word_other`是有词没deriv，`word_no_res`是没词
    3.3 放弃`word_no_res`，去`etymonline`上爬取`word_other`，查找里面的<div class="word--C9UPa">（每一个条目是一个意思）。具体用`etym_crawler.crawl_list`实现
    