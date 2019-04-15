# 新浪微博爬虫

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/weibo-crawler/blob/master/README-cn.md)

基于**Python**实现的新浪微博爬虫，用于爬取某用户的微博数据（文本，JPG/GIF图片和视频）。

特别鸣谢[Python中文社区](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627)提供的原始代码`SourceCode_weibocrawler.py`。

## 功能

- 爬取原创和转发微博中的**文本**。

- 爬取原创和转发微博中的**JPG/GIF图片**。

- 爬取原创和转发微博中的**视频**。

## 依赖项

* __requests 2.21.0__
* __lxml 4.2.5__

## 使用方法

1. 参考程序注释，设置爬虫的参数（`WEBSITE_HEADERS`，`PAGE_AMOUNT`，等）。

2. 运行`run_WeiboCrawler.py`程序文件，爬取指定用户的微博数据。

3. 爬取的数据将会保存在设定的文件目录下（例如，`/WeiboData_JJY`）。

    1. 爬取的文本将会保存于TXT文件（例如，`/WeiboData_JJY/JJY_Weibo_PostRecords.txt`）。

    2. 爬取的图片和视频将会保存于单独的子文件夹。

<br>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。^_^</i>

<i>最后更新：15/04/2019</i>
