# Weibo Data Crawling

This is the **Python** implementation of crawling Weibo data (i.e., posted text, jpg/gif images and videos) of one user.

The source code (see [SourceCode_weibocrawler.py](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/SourceCode_weibocrawler.py)) is forked from: https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627.

* Removed function: Crawl comments of Weibo posts.

* Added function: Crawl gif images and videos in both original and retweeted Weibo posts.

# Environment

The code has been tested on **Ubuntu 16.04**.

# Language

* __Python 3.7 (3.0+)__

# Running

* Specify user settings in ```WeiboDataCrawling_ALL.py``` file (Line 17~22).

* To crawl **text**, **jpg/gif images** and **videos** data, excute the following command on Terminal:
```bash
~$ python WeiboDataCrawling_ALL.py
```
* Weibo data will be saved in your specified folder (e.g., WeiboData_JuJingyi_20190119/).

# Motivation

XDDD

![Equivariance](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/JuJingyi.jpg)
