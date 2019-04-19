# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

This is a **Python** implementation of crawling Weibo data (e.g., text, images, live photos, and videos) of one Sina Weibo user from [Weibo Mobile Client](https://m.weibo.cn). It simulates user login with **session** (username and password).

Many thanks to [Python Chinese Community](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627) for providing the source code `SourceCode_weibocrawler.py`.

## Functions

- Crawling the short or long **text** in original and retweeted Weibo posts.

- Crawling the large (preferred) or small **JPG/GIF images** in original and retweeted Weibo posts.

- Crawling the **live photos** (as JPG images, MOV videos and/or GIF images) in original and retweeted Weibo posts.

- Crawling the HD (preferred) or SD **videos** in original and retweeted Weibo posts.

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__
* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## Usage

### User Settings

1. Set `S_DATA` and `S_HEADER` of session for simulating user login (see comments for obtaining those information).

2. Set `USER_URL` of target Sina Weibo user (see comments for obtaining this information).

3. Set `PAGE_AMOUNT` the amount of pages for crawling. It is greater than 10% of the amount of user's Weibo posts.

4. Set `PATH_FOLDER` and `PATH_FILE_TXT` for saving Weibo data.

5. Select the type of Weibo data for crawiling (`IF_IMAGE`, `IF_PHOTO`, and `IF_VIDEO`). '0' - No, '1' - Yes.

6. Set `IF_LIVE2GIF = 1` if live photos (MOV videos) need to be converted to GIF images.

### Run

1. Run `run_WeiboCrawler.py` to crawl Weibo data of one Sina Weibo user.

2. See `Log_run_WeiboCrawler.txt` for log information of running this code.

### Results

1. The Weibo data will be saved in the pre-specified folder (e.g., `JJY_WeiboData/`).

2. The text of Weibo posts will be saved in the TXT file (e.g., `JJY_WeiboData/JJY_WeiboPost_Records.txt`).

3. The images, photos, and videos will be saved in sub-folders (e.g., `1/`, `1_livephoto/`, `1_video/`).

<br>

<i>Please report an issue if you have any problem using this repository, I will respond ASAP.</i>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>
a
