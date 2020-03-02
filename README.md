# Sina Weibo Crawler

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

This is a **Python** implementation of crawling Weibo data (e.g., text, images, live photos, and videos) of target Sina Weibo user from the [Weibo Mobile Client](https://m.weibo.cn). It simulates user login with the **session** (username and password).

Many thanks to [Python Chinese Community](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627) for providing the source code `SourceCode_weibocrawler.py`.

## Functions

- Crawling **short text** in original and retweeted Weibo posts.

- Crawling large (preferred) or small **JPG/GIF images** in original and retweeted Weibo posts.

- [**New!**] Crawling **live photos** (as JPG images, MOV videos, and/or GIF images) in original and retweeted Weibo posts.

- Crawling HD (preferred) or SD **videos** in original and retweeted Weibo posts.

## Environment

This code has been tested on Ubuntu 16.04 operating system. For Windows and macOS, the format of folder path should be changed accordingly.

## Dependencies

* __requests 2.21.0__
* __lxml 4.2.5__
* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## Usage

### User Settings

1. Set `S_DATA` and `S_HEADER` of the session for simulating Sina Weibo user login (see comments for details).

2. Set `USER_URL` of the target Weibo user (see comments for details).

3. Set the amount of pages (`PAGE_AMOUNT`) for crawling (see comments for details).

4. Set the path (`PATH_FOLDER`) and the TXT file (`PATH_FILE_TXT`) for saving Weibo data.

5. Set the type of Weibo data (`IF_IMAGE`, `IF_PHOTO`, and `IF_VIDEO` as `1`) for crawling.

6. Set `IF_LIVE2GIF = True` if live photos (videos) need to be converted to GIF images.

7. Set `TIME_DELAY` of the crawler to avoid `ConnectionError 104: ('Connection aborted.')`.

8. If `ConnectionError 104: ('Connection aborted.')` occurs:

   1. Set `IF_RECONNECT = True` for running the crawler in **reconnection mode**.

   2. Set `TAG_STARTCARD` as the serial number of the stopping Weibo post (according to log information).

   3. Re-run `run_WeiboCrawler.py` to continue to crawl Weibo data.

   4. Set `IF_RECONNECT = False` if run the crawler in **normal mode**!

### Run

1. Run `run_WeiboCrawler.py` to crawl Weibo data of the target Sina Weibo user.

2. See `Log_run_WeiboCrawler.txt` for log information of running the code.

### Results

1. The Weibo data will be saved in the pre-specified folder (e.g., `Demo_WeiboData/`).

2. The text of Weibo posts will be saved in the TXT file (e.g., `Demo_WeiboData/Demo_WeiboPost_Records.txt`).

3. The images, live photos, and videos will be saved in sub-folders (e.g., `1/`, `1_livephoto/`, and `1_video/`).

<br>

<i>Please report an issue if you have any question about this repository, I will respond ASAP.</i>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>
