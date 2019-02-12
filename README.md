# Weibo Data Crawler

This is a **Python** implementation of crawling Sina Weibo data (e.g., text, images, and videos) of one user.

The source code [SourceCode_weibocrawler.py](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/SourceCode_weibocrawler.py) is forked from: https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627.

### Added functions: 

1. Crawl gif images in both original and retweeted Weibo posts.

2. Crawl videos in both original and retweeted Weibo posts.

### Removed function: 

1. Crawl comments of Weibo posts.

## Environment

The code has been tested on **Ubuntu 16.04** operating system.

## Language

* __Python 3.7 (3.0+)__

## Running

* Specify user settings in ```WeiboDataCrawling_ALL.py``` file (see line 17~22).

* To crawl **text**, **jpg/gif images** and **videos** data, excute the following command on Terminal:
```bash
~$ python WeiboDataCrawling_ALL.py
```
* Weibo data will be saved in your specified folder (e.g., WeiboData_JuJingyi_20190119/).

## Motivation

XDDD

![Equivariance](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/JuJingyi.jpg)

<i>Last updated: 11/02/2019</i>
