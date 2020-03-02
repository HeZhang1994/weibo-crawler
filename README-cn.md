# 新浪微博爬虫

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

基于**Python**实现的从[微博移动端](https://m.weibo.cn/)爬取目标新浪微博用户的微博数据（文本、图片、实况照片和视频）。该爬虫通过session（用户名和密码）模拟用户登录。

特别感谢[Python中文社区](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627)提供的原始代码`SourceCode_weibocrawler.py`。

## 功能

- 爬取原创和转发微博中的**短文本**。

- 爬取原创和转发微博中的大（优先）或小**JPG/GIF图片**。

- [**新!**] 爬取原创和转发微博中的**实况照片**（存为JPG图片、MOV视频和/或GIF图片）。

- 爬取原创和转发微博中的高清（优先）或标清**视频**。

## 环境

爬虫程序在Ubuntu 16.04操作系统已测试通过。针对Window和macOS操作系统，文件路径的格式需要进行相应的修改。

## 依赖项

* __requests 2.21.0__
* __lxml 4.2.5__
* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## 使用方法

### 用户设置

1. 设置session的`S_DATA`和`S_HEADER`以模拟新浪微博用户登录（详细信息参见注释）。

2. 设置目标微博用户的`USER_URL`（详细信息参见注释）。

3. 设置爬取的总页数`PAGE_AMOUNT`（详细信息参见注释）。

4. 设置保存微博数据的路径`PATH_FOLDER`和文本文件`PATH_FILE_TXT`。

5. 设置爬取的微博数据类型（`IF_IMAGE`、`IF_PHOTO`和`IF_VIDEO`为`1`）。

6. 若需要将实况照片（视频）转换为GIF图片，设置`IF_LIVE2GIF = True`。

7. 设置爬虫的`TIME_DELAY`以避免`ConnectionError 104: ('Connection aborted.')`。

8. 如果出现`ConnectionError 104: ('Connection aborted.')`：

   1. 设置`IF_RECONNECT = True`以**重连模式**运行爬虫。

   2. 设置`TAG_STARTCARD`为终止微博的序号（根据日志信息）。

   3. 重新运行`run_WeiboCrawler.py`以继续爬取微博数据。

   4. 若以**正常模式**运行爬虫，设置`IF_RECONNECT = False`！

### 运行

1. 运行`run_WeiboCrawler.py`，以爬取目标新浪微博用户的微博数据。

2. 运行该程序的日志信息参见`Log_run_WeiboCrawler.txt`。

### 结果

1. 微博数据将会保存在预设定的文件夹（例如，`Demo_WeiboData/`）。

2. 微博文本将会保存于文本文件（例如，`Demo_WeiboData/Demo_WeiboPost_Records.txt`）。

3. 图片、实况照片和视频将会保存于子文件夹（例如，`Demo_WeiboData/1/`、`Demo_WeiboData/1_livephoto/`和`Demo_WeiboData/1_video/`）。

<br>

<i>如果您对该项目有任何问题，请报告issue，我将会尽快回复。</i>

<i>如果该项目对您有帮助，请为其加星支持哈，非常感谢。^_^</i>
