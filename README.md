# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This is a **Python** implementation of crawling Sina Weibo data (e.g., text, JPG/GIF images, and videos) of one Weibo user.

Many thanks to [Python Chinese Community](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627) for providing the source code `SourceCode_weibocrawler.py`.

## Functions

- Crawling the **text** in the original and re-tweeted Weibo posts.

- Crawling the **JPG/GIF images** in the original and re-tweeted Weibo posts.

- Crawling the **videos** in the original and re-tweeted Weibo posts.

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__

## Usage

1. Specify user settings (`WEBSITE_HEADERS`, `PAGE_AMOUNT`, etc.) in the code (see comments).

2. Run `run_WeiboCrawler.py` to crawl Weibo data of target Weibo user.

3. The Weibo data will be saved in the pre-specified folder (e.g., `/WeiboData_JJY`).

    1. The text of posts will be saved in a TXT file (see `/WeiboData_JJY/JJY_Weibo_PostRecords.txt` as an example).
  
    2. The images and videos of posts will be saved in separated folders.

<br>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。^_^</i>

<i>Last updated: 07/04/2019</i>
