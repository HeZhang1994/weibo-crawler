# 新浪微博爬虫

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

基于**Python**实现的爬取某用户的新浪微博数据（文本，图片，实况照片和视频）。

特别鸣谢[Python中文社区](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627)提供的原始代码`SourceCode_weibocrawler.py`。

## 功能

- 爬取原创和转发微博中的短或长**文本**。

- 爬取原创和转发微博中的大（优先）或小**JPG/GIF图片**。

- 爬取原创和转发微博中的**实况照片**（为MOV视频或GIF图片）。

- 爬取原创和转发微博中的高清（优先）或标清**视频**。

## 依赖项

* __requests 2.21.0__
* __lxml 4.2.5__
* __cv2 4.1.0__
* __imageio 2.4.1__
* __PIL 5.3.0__

## 使用方法

1. 参考程序注释，设置爬虫的参数（`WEBSITE_HEADERS`，`USER_URL`，`PAGE_AMOUNT`，等）。

2. 运行`run_WeiboCrawler_v1.py`，爬取某用户的微博数据（日志信息参见`Log_run_WeiboCrawler.txt`）。

3. 微博数据将会保存在预设定的文件夹（例如，`JJY_WeiboData/`）。

    1. 文本将会保存于TXT文件（例如，`JJY_WeiboData/JJY_WeiboPost_Records.txt`）。

    2. 图片、照片和视频将会保存于单独的子文件夹。

<br>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。^_^</i>
