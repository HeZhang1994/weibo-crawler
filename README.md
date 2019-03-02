# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This is a **Python** implementation for crawling Sina Weibo data (e.g., text, images, and videos) of one Weibo user.

The source code ```SourceCode_weibocrawler.py``` is forked from [here](https://www.researchgate.net/publication/305696390_Game_Theoretic_Hypergraph_Matching_for_Multi-source_Image_Correspondences).

## Functions

- Crawl **text** in original and re-tweeted Weibo posts.

- Crawl **JPG/GIF images** in original and re-tweeted Weibo posts.

- Crawl **videos** in original and re-tweeted Weibo posts.

## Usage

1. Specify settings of targeted Weibo user in ```WeiboDataCrawling_ALL.py``` (see instruction on line 17~22).

2. To crawl **text**, **JPG/GIF images** and **videos** data, execute the following command in Terminal.
```bash
~$ python WeiboDataCrawling_ALL.py
```

3. Weibo data will be saved in pre-specified folder (e.g., ```WeiboData_JuJingyi_20190119/```).

## Motivation

XD

<!--![Equivariance](https://github.com/HeZhang1994/weibo-data-crawling/blob/master/JuJingyi.jpg)-->

<br>

<i>Please star this repository if you found its content useful. Thank you very much.</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。</i>

<i>Last updated: 25/02/2019</i>

