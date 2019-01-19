# Weibo Data Crawling

This is the Python implementation of crawling Weibo data (i.e., posted text, jpg/gif images and videos) of one Weibo user.

The source code (SourceCode_weibocrawler.py) is forked from: https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627.

* Removed function: Crawl comments of posts.

* Added function: Crawl gif images and videos in original and transfered posts.

# Environment

The code has been tested on **Ubuntu 14.04**. 

# Language

* __Python 3.5 (3.0+)__

# Running

* Specify user settings in ```WeiboDataCrawling_ALL.py``` file in .

* To crawl **text**, **jpg/gif images** and **videos**, excute the following command on Terminal:
```bash
$ python WeiboDataCrawling_ALL.py
$ # or
$ python3 WeiboDataCrawling_ALL.py
$ # if both py2 and py3 exist on your operating system.
```
The Weibo data will be saved in user specified folder (e.g., WeiboData_JuJingyi_20190119/).

# Motivation

XDDD

![Equivariance](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/JuJingyi.jpg)
