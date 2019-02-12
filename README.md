# Weibo Data Crawler

This is a **Python** implementation of crawling Sina Weibo data (e.g., text, images, and videos) of one user.

The source code [SourceCode_weibocrawler.py](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/SourceCode_weibocrawler.py) is forked from: https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627.

### Functions

1. Crawl **text** in original and re-tweeted Weibo posts.

2. Crawl **jpg/gif images** in original and re-tweeted Weibo posts.

3. Crawl **videos** in original and re-tweeted Weibo posts.

### Limitation

1. Can not crawl comments of Weibo posts (removed from source code).

## Environment

The code has been tested on **Ubuntu 16.04** operating system.

## Language

* __Python 3.7 (3.0+)__

## Usage

* Specify settings of targeted user in ```WeiboDataCrawling_ALL.py``` file (see line 17~22).

* To crawl **text**, **jpg/gif images** and **videos** data, execute the following command on Terminal:
```bash
~$ python WeiboDataCrawling_ALL.py
```

* Weibo data will be saved in pre-specified folder (e.g., WeiboData_JuJingyi_20190119/).

## Motivation

XD

![Equivariance](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/JuJingyi.jpg)

<i>Last updated: 12/02/2019</i>
