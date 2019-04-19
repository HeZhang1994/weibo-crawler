# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

This is a **Python** implementation of crawling Sina Weibo data (e.g., text, images, live photos, and videos) of one user.

Many thanks to [Python Chinese Community](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627) for providing the source code `SourceCode_weibocrawler.py`.

## Functions

- Crawling the short or long **text** in original and retweeted Weibo posts.

- Crawling the large (preferred) or small **JPG/GIF images** in original and retweeted Weibo posts.

- Crawling the **live photos** (as MOV videos and/or GIF images) in original and retweeted Weibo posts.

- Crawling the HD (preferred) or SD **videos** in original and retweeted Weibo posts.

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__
* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## Usage

1. Specify user settings (`WEBSITE_HEADERS`, `USER_URL`, `PAGE_AMOUNT`, etc.) in the code (see comments).

2. Run `run_WeiboCrawler.py` to crawl Weibo data of one user (see `Log_run_WeiboCrawler.txt` for log information).

3. The Weibo data will be saved in the pre-specified folder (e.g., `JJY_WeiboData/`).

    - The text of will be saved in a TXT file (see `JJY_WeiboPost_Records.txt` as an example).

    - The images, photos, and videos will be saved in separated sub-folders.

<br>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>
