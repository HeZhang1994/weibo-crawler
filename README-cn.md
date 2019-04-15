# 新浪微博爬虫

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/weibo-crawler/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

基于Python实现的网站爬虫，用于爬取某新浪微博用户的数据（文本，JPG/GIF图片和视频）。

特别鸣谢[Python中文社区](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/79547627)提供的原始代码`SourceCode_weibocrawler.py`。

## 功能

- 爬取原创和转发微博的**文本**。

- 爬取原创和转发微博的**JPG/GIF图片**。

- 爬取原创和转发微博的**视频**。

## 依赖

* __requests 2.21.0__
* __lxml 4.2.5__

## 使用

1. 参考程序注释，设置爬虫的参数（`WEBSITE_HEADERS`，`PAGE_AMOUNT`，等）。

2. 运行`run_WeiboCrawler.py`程序文件，爬取指定用户的微博数据。

3. 用户的微博数据将会保存在之前制定的文件目录下（例如，`/WeiboData_JJY`）。

    1. 微博数据中的文本将会保存在TXT文件中（以`/WeiboData_JJY/JJY_Weibo_PostRecords.txt`为例）。

    2. 微博数据中的图片和视频将会保存在单独的子文件夹中。

<br>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。^_^</i>

<i>Last updated: 15/04/2019</i>
