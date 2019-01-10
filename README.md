# Weibo Data Crawling

This is the Python implementation of crawling Weibo data (i.e., posted text, images and videos) of one Weibo user.

The source code (SourceCode_weibocrawler.py) is forked from: https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627.

Notes: We remove the function of crawling comments and add the function of crawling videos.

# Environment

* __Ubuntu 14.04__

# Language

* __Python 3.5.2__

# Running

* Empty saving folder (i.e., JuJingyi_Weibo_TI/ or JuJingyi_Weibo_TIV/) before running code!

* To crawl **text** and **images**, excute the following command on Terminal:
```bash
$ python3 WeiboDataCrawling_TextImage.py
```
The Weibo data will be saved in JuJingyi_Weibo_TI/ folder.

* To crawl **text**, **images** and **videos**, excute the following command on Terminal:
```bash
$ python3 WeiboDataCrawling_TextImageVideo.py
```
The Weibo data will be saved in JuJingyi_Weibo_TIV/ folder.

# Motivation

XDDD

![Equivariance](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/JuJingyi.jpg)
