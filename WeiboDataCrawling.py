## Task description:
## Crawl Weibo information (posted text and images) of one specific Weibo user.
## Example: Ju Jingyi (https://m.weibo.cn/u/3669102477).

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
'Cookie': 'XXXXXXXXXXXXXXX',
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
# The "Cookie" might be changed in 3` hours and should be updated accordingly!!!
# The "Referer" should be changed for different weibo user!!!

user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'
# The "user_url" can be obtained as below: 
# -> DevTools (F12) -> "XHR" -> Refresh webpage (F5)
# -> select "getindex?type..." in "Name" -> "Headers"
# -> "General" -> "Request URL" -> done.

user_name = 'JuJingyi'

page = 60
# page (int): Total pages for crawling.

# Note: 
# There are 13` posts on one Weibo page.
# Set "page" = total posts/13.
# Example for Ju Jingyi, "page" = 808`/13.


## Obtain the list of "card" information on specified pages.

ii = 0  # Serial number of pages.
list_cards = []  # Store "card" information.
while ii < page:
    ii = ii + 1
    print('Start crawling all cards on page %d ...' % ii)
    url = user_url + '&page=' + str(ii-1)  
    # Note: [ii-1] The serial number of Weibo pages starts from 0!!!
    
    response = requests.get(url, headers=headers)
    ob_json = json.loads(response.text)  
    # ob_json (dict)
    
    list_cards.append(ob_json['data']['cards'])  
    # ob_json['data']['cards'] (list)
    
    print('... Finished.')
    
    time.sleep(2)
    print('Suspend 5 seconds.' + '\n' + 30 * '-')
    print('\n')
    # Suspend 2 seconds after crawling cards on one page.


## Crawl Weibo data (posted text and images).

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
            
            # Save posted text.
            with open(path + 'weibo_crawl.txt', 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_weibo) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')
            
            # Save posted imgaes.
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
        
        time.sleep(2)
        print('Suspend 2 seconds.\n')  
        # Suspend 2 seconds after crawling one Weibo post.
    
    page_weibo = page_weibo + 1
    print('... Completed.')
