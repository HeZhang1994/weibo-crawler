# 新浪微博爬虫

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

基于**Python**实现的从[微博移动端](https://m.weibo.cn/)爬取某新浪微博用户的微博数据（文本、图片、实况照片和视频）。该爬虫通过session（用户名和密码）模拟用户登录。

特别鸣谢[Python中文社区](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627)提供的原始代码`SourceCode_weibocrawler.py`。

## 功能

- 爬取原创和转发微博中的短或长**文本**。

- 爬取原创和转发微博中的大（优先）或小**JPG/GIF图片**。

- [**新!**] 爬取原创和转发微博中的**实况照片**（为JPG图片、MOV视频和/或GIF图片）。

- 爬取原创和转发微博中的高清（优先）或标清**视频**。

## 依赖项

* __requests 2.21.0__
* __lxml 4.2.5__
* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## 使用方法

### 用户设置

1. 设置session的`S_DATA`和`S_HEADER`以模拟用户登录（获取信息参见程序注释）。

2. 设置目标新浪微博用户的`USER_URL`（获取信息参见程序注释）。

3. 设置爬取的总页数`PAGE_AMOUNT`。该参数大于用户微博总数的10%。

4. 设置保存微博数据的`PATH_FOLDER`和`PATH_FILE_TXT`。

5. 选择爬取的微博数据类型（`IF_IMAGE`、`IF_PHOTO`和`IF_VIDEO`）。 0 - 不爬取, 1 - 爬取.

6. 设置`IF_LIVE2GIF = 1`如果需要将实况照片（MOV视频）转换为GIF图片。

### 运行

1. 运行`run_WeiboCrawler_v1.py`以爬取某新浪微博用户的微博数据。

2. 程序运行的日志信息参见`Log_run_WeiboCrawler.txt`。

### 结果

1. 微博数据将会保存在预设定的文件夹（例如，`JJY_WeiboData/`）。

2. 微博文本将会保存于TXT文件（例如，`JJY_WeiboData/JJY_WeiboPost_Records.txt`）。

3. 图片、照片和视频将会保存于子文件夹（例如，`1/`、`1_livephoto/`和`1_video/`）。

<br>

<i>如果您对该项目有任何问题，请报告issue，我将会尽快回复。</i>

<i>如果该项目对您有帮助，请为其加星支持哈，非常感谢。^_^</i>
