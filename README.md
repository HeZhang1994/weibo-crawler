# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This is a **Python** implementation of crawling Sina Weibo data (e.g., posted/re-tweeted text, JPG/GIF images, and videos) of one Weibo user.

The source code ```SourceCode_weibocrawler.py``` is forked from [here](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627).

## Functions

- Crawling **text** in original and re-tweeted Weibo posts.

- Crawling **JPG/GIF images** in original and re-tweeted Weibo posts.

- Crawling **videos** in original and re-tweeted Weibo posts.

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__

## Usage

1. Specify user settings in ```run_WeiboCrawler.py``` (see code comments for details).

2. Run ```run_WeiboCrawler.py```.

3. The Weibo data will be saved in the pre-specified folder (e.g., ```WeiboData_JJY/```).

<br>

<i>Please star this repository if you found its content useful. Thank you very much.</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。</i>

<i>Last updated: 16/03/2019</i>

