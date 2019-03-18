# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This is a **Python** implementation of crawling Sina Weibo data (e.g., posted/re-tweeted text, JPG/GIF images, and videos) of one Weibo user.

Thanks a lot for the source code `SourceCode_weibocrawler.py` released by [Python Chinese Community](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627).

## Functions

- Crawling **text** in the original and re-tweeted Weibo posts.

- Crawling **JPG/GIF images** in the original and re-tweeted Weibo posts.

- Crawling **videos** in the original and re-tweeted Weibo posts.

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__

## Usage

1. Specify user settings (e.g., `WEBSITE_HEADERS`, `USER_URL`, and `PAGE_AMOUNT`) in the code (see comments for details).

2. Run `run_WeiboCrawler.py` to crawl Weibo data.

3. The Weibo data will be saved in the pre-specified folder (e.g., `WeiboData_JJY/`).

<br>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。^_^</i>

<i>Last updated: 18/03/2019</i>
