# -*- coding:utf-8 -*-
'''
Created on 2018年3月9日

@author: ora_jason
'''
from lxmlimport html
import requests
import json
import re
import os
import time
import urllib.request


class CrawlWeibo:
# 获取指定博主的所有微博cards的list
defgetCards(self, id, page):  # id（字符串类型）：博主的用户id；page（整型）：微博翻页参数
ii = 0
list_cards = []
while ii < page:
            ii = ii + 1
print('正在爬取第%d页cards' % ii)
url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=107603' + id + '&page=' + str(
                ii)
            response = requests.get(url, headers=headers)
ob_json = json.loads(response.text)  # ob_json为dict类型

list_cards.append(ob_json['data']['cards'])  # ob_json['data']['cards']为list类型
time.sleep(2)
print('暂停2秒')  # 爬完一页所有微博的cards后 停顿两秒
return list_cards# 返回所有页的cards

    # 获取某条微博的热门评论或评论的list
defgetComments(self, id, page):  # id（字符串类型）：某条微博的id；page（整型）：评论翻页参数
url = 'https://m.weibo.cn/api/comments/show?id=' + id + '&page=' + str(page)
        response = requests.get(url, headers=headers)
ob_json = json.loads(response.text)

list_comments = []
if 'data' in ob_json:
if 'hot_data' in ob_json['data']:
list_comments = ob_json['data']['hot_data']
else:
list_comments = ob_json['data']['data']
return list_comments# 返回某条微博下评论

defgetAll(self, id, page, path):  # id为博主uid，page为爬取页数，path为保存路径
list_cards = self.getCards(id, page)
print('爬取页数为：' + str(len(list_cards)) + '\n' + 30 * '-')
count_weibo = 1
page_weibo = 1
# 遍历当页所有微博，保存内容，并根据id查找输出热门评论
for cards in list_cards:
for card in cards:
if card['card_type'] == 9:  # 过滤出微博
#if card['card_type'] == 9 and 'raw_text' not in card['mblog']:  # 过滤出原创微博
print('正在爬取第' + str(page_weibo) + '页 第' + str(count_weibo) + '条card')
                    mid = card['mblog']['id']
created_at = card['mblog']['created_at']
# 获取保存文本信息
if card['mblog']['isLongText'] == 'false':
                        text = card['mblog']['text']
else:
url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                        response = requests.get(url, headers=headers)
ob_json = json.loads(response.text)  # ob_json为dict类型
text = ob_json['data']['longTextContent']
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')  # 用string函数过滤掉多余标签
# 输出微博文本
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
ff.write('第' + str(count_weibo) + '条\n' + '***  发布于  ' + created_at + '  ***' + '\n')
ff.write(text + '\n')

# 获取保存图片
if 'bmiddle_pic' in card['mblog']:
image_path = path + str(count_weibo)
# if os.path.exists(image_path) is False:
os.mkdir(image_path)
url_extend = 'https://m.weibo.cn/status/' + mid  # 单条微博url
res = requests.get(url_extend, headers=headers).text  # str类型
imgurl_weibo = re.findall('https://.*large.*.jpg', res)  # 用正则匹配到图片url
x = 1
for iin range(len(imgurl_weibo)):
                            temp = image_path + '/' + str(x) + '.jpg'
# 将图片url添加到微博文本中
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
ff.write('微博图片链接：' + imgurl_weibo[i] + '\n')
print('正在下载该条微博 第%s张图片' % x)
try:
                                urllib.request.urlretrieve(urllib.request.urlopen(imgurl_weibo[i]).geturl(), temp)
except:
print("该图片下载失败:%s" % imgurl_weibo)
                            x += 1
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
ff.write(78 * '-' + '评论' + '>' + 78 * '-' + '\n')
else:
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
ff.write(78 * '-' + '评论' + '>' + 78 * '-' + '\n')
count_weibo = count_weibo + 1

# 根据微博id获取热门评论，并输出
list_comments = self.getComments(mid, 1)  # 评论只需要访问第一页
print('正在爬取该条微博 评论')
count_hotcomments = 1
for comment in list_comments:
# like_counts = comment['like_counts']  # 点赞数
text = comment['text']  # 评论内容
tree = html.fromstring(text)
                        text = tree.xpath('string(.)')  # 用string函数过滤掉多余标签
name_user = comment['user']['screen_name']  # 评论者的用户名
# 输出评论数据
if count_hotcomments<len(list_comments):
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
                                result = str(count_hotcomments) + ': #' + name_user + '#'
ff.write(result + '\n')
ff.write(text + '\n\n')
else:
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
                                result = str(count_hotcomments) + ': #' + name_user + '#'
ff.write(result + '\n')
ff.write(text + '\n')
count_hotcomments = count_hotcomments + 1
with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
ff.write(78 * '-' + '<' + '评论' + 78 * '-' + '\n\n\n\n')
time.sleep(2)
print('暂停2秒\n')  # 爬完一条微博的所有内容后 停顿两秒
page_weibo = page_weibo + 1


# 请求头，爬取新博主需更新Cookie和Referer
headers = {
'Cookie': '_T_WM=5a5b9ae925e458f93279d6708b159927; ALF=1523107054; SCF=Ativ2ybI8StjZccoSRca_uyzfWFIcM45JHEaLQ_tD8ksmi6-whOM5Pl1p8Vz4EziyMQe5QgrSlo8RY9Nd3NiFO8.; SUB=_2A253pUizDeRhGeRG61EV9S_NwzuIHXVVZmj7rDV6PUJbktANLXD4kW1NTeA_GStZpY6CFmR1PzgN50YL186u9HbC; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2V9E8BT6Glu5-SxvF-MwO5JpX5K-hUgL.FozReheXSK2p1hM2dJLoI7D29PyXUGxXUsHE; SUHB=02M_R-ArnK_FEZ; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D3900009063730800%26luicode%3D10000011%26lfid%3D1076031195054531%26fid%3D1005051195054531%26uicode%3D10000011',
'Host': 'm.weibo.cn',
# 'qq': 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
'Referer': 'https://m.weibo.cn/u/1195054531',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

crawl_weibo = CrawlWeibo()  # 实例化爬虫类并调用成员方法进行输出
crawl_weibo.getAll('1195054531', 2, 'D:/weibo/')  # 输入需要爬取用户uid，需要爬取微博页数，微博本地保存路径
