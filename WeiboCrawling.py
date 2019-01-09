## Task description:
## Crawl Weibo information (text and images) of a specific Weibo user.
## Target Weibo user: Ju Jingyi (https://m.weibo.cn/u/3669102477)

## Requirement: Python 3.0+.

from lxml import html
import requests
import json
import re
import os
import time
import urllib.request


## Set webpage request headers.

headers = {
'Cookie': '_T_WM=0156a969cd38bad059e03fa25ed5efb0; WEIBOCN_FROM=1110006030; SUB=_2A25xMRjwDeRhGeBG6lAY8CjOzz2IHXVS3bi4rDV6PUJbktBeLW3wkW1NRjEq90xz37m6Wn6vNpYT6KYktvnM-jiX; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhC2nHyIKl8-x_yG3nPvgYm5JpX5KzhUgL.FoqReKz4ehqESh22dJLoIX5LxK-L1h-LBoBLxKnLBoqLBKeLxK-LBo.LB.qLxKqLBoeL1-zLxKML1-2L1hxZi--fiKy2iKLWi--fi-20i-8F; SUHB=0u5R0_BCrYn4gH; SSOLoginState=1547004064; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D10760336691024773669102477%26fid%3D1005053669102477%26uicode%3D10000011',
'Host': 'm.weibo.cn',
'Referer': 'https://m.weibo.cn/u/3669102477',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
# The information of "headers" can be obtained as below:
# -> DevTools (F12) -> "XHR" -> Refresh webpage (F5)
# -> select "getindex?type..." in "Name" -> "Headers"
# -> "Request Headers" -> ... -> done.

# Note: 
# The "Cookie" is obtained from https://m.weibo.cn/u/3669102477 (login required).
# The "Cookie" might be changed in hours and should be updated accordingly!!!
# The "Referer" should be changed for different weibo user!!!

user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'
# The "user_url" can be obtained as below: 
# -> DevTools (F12) -> "XHR" -> Refresh webpage (F5)
# -> select "getindex?type..." in "Name" -> "Headers"
# -> "General" -> "Request URL" -> done.

user_name = 'JuJingyi'

page = 60  
# page (int): Specified pages for crawling.

# Note: 
# There are 13 posts on one page.
# Set "page" = total posts/13.
# For Ju Jingyi, "page" = 808/13.


## Obtain the list of "card" information on specified pages.

ii = 0  # Serial number of pages.
list_cards = []  # Store "card" information.
while ii < page:
    ii = ii + 1
    print('Start crawling all cards on page %d ...' % ii)
    url = user_url + '&page=' + str(ii-1)  
    # Note: The serial number of Weibo pages starts from 0!!!
    
    response = requests.get(url, headers=headers)
    ob_json = json.loads(response.text)  
    # ob_json (dict)
    
    list_cards.append(ob_json['data']['cards'])  
    # ob_json['data']['cards'] (list)
    
    print('... Finished.')
    
    time.sleep(5)
    print('Suspend 5 seconds.' + '\n' + 30 * '-')
    print('\n')
    # Suspend 5 seconds after crawling cards on one page.


## Crawl Weibo data (text and images).

print(40 * '=' + '\n' + 'The number of pages for crawling is: ' + str(len(list_cards)) + '.' + '\n' + 40 * '=' + '\n')

count_weibo = 1  # Serial number of cards.
page_weibo = 1  # Serial number of pages.

path = user_name + '_Weibo/'  
# Path for saving all Weibo information.
# Note: The path should be empty before crawling!!!

for cards in list_cards:
    for card in cards:
        if card['card_type'] == 9:
            
            print('\n')
            print('Start crawling the ' + str(count_weibo) + '-th card on ' + str(page_weibo) + '-th page.')
            
            mid = card['mblog']['id']
            created_at = card['mblog']['created_at']
            
            # Crawl Weibo posts information.
            if card['mblog']['isLongText'] == 'false':
                text = card['mblog']['text']
            else:
                url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                response = requests.get(url, headers=headers)
                ob_json = json.loads(response.text)  # ob_json (dict)
                text = ob_json['data']['longTextContent']
                tree = html.fromstring(text)
                text = tree.xpath('string(.)')
            
            # Save text of posts.
            with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_weibo) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')
            
            # Save imgae of posts.
            if 'bmiddle_pic' in card['mblog']:
                image_path = path + str(count_weibo)
                os.mkdir(image_path)
                url_extend = 'https://m.weibo.cn/status/' + mid  # URL of one Weibo post.
                res = requests.get(url_extend, headers=headers).text  # (string)
                imgurl_weibo = re.findall('https://.*large.*.jpg', res)  # Match URL of image.
                x = 1
                for i in range(len(imgurl_weibo)):
                    temp = image_path + '/' + str(x) + '.jpg'
                    # Add image URL to text file.
                    with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
                        ff.write('The link of image is：' + imgurl_weibo[i] + '\n')
                    print('Download the %s-th image of this weibo.' % x)
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imgurl_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download %s-th image." % imgurl_weibo)
                    x += 1
        
        count_weibo = count_weibo + 1
        print('... Finished.')
        
        time.sleep(5)
        print('Suspend 5 seconds.\n')  
        # Suspend 5 seconds after crawling one Weibo post.
    
    page_weibo = page_weibo + 1
    print('... Completed.')
