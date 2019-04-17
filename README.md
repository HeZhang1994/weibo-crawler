# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

This is a **Python** implementation of crawling Sina Weibo data (e.g., text, JPG/GIF images, live photos, and videos) of one Weibo user.

Many thanks to [Python Chinese Community](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627) for providing the source code `SourceCode_weibocrawler.py`.

## Functions

- Crawling the **text** in original and retweeted Weibo posts.

- Crawling the **JPG/GIF images** in original and retweeted Weibo posts.

- Crawling the **videos** in original and retweeted Weibo posts.

- **[New!]** Crawling the **live photos** in original and retweeted Weibo posts (as GIF image and MOV video).

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__

The following dependencies are used for crawling live photos.

* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## Usage

1. Specify user settings (`WEBSITE_HEADERS`, `PAGE_AMOUNT`, etc.) in the code (see comments).

2. Run `run_WeiboCrawler_v1.py` to crawl Weibo data of target Weibo user **without** live photos.

3. Run `run_WeiboCrawler_v2.py` to crawl Weibo data of target Weibo user **with** live photos.

4. The Weibo data will be saved in the pre-specified folder (e.g., `/WeiboData_JJY`).

    1. The text of posts will be saved in a TXT file (see `/WeiboData_JJY/JJY_Weibo_PostRecords.txt` as an example).

    2. The images and videos of posts will be saved in separated sub-folders.

<br>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>
