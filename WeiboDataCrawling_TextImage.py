## Task description:
## Crawl Weibo data (posted text and images) of one Weibo user.
## Example: Ju Jingyi (https://m.weibo.cn/u/3669102477).

## Requirement: Python 3.0+.


from lxml import html
import requests
import json
import re
import os
import time
import urllib.request


## Part 1 Set webpage request headers.

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
# The "Cookie" might be changed in hours and should be updated accordingly!!!
# The "Referer" should be changed for different Weibo user!!!

# Question: 
# By setting 'Cookie': "XXX...XXX", why the code can still crawl Weibo data???
# Answer:
# This code only crawls Weibo data (text, images and videos) that can be accessed by visitor (non-login).
# If this code need to crawl Weibo comments, "Cookie" is required (login).

user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'

# The information of "user_url" can be obtained as below:
# -> DevTools (F12) -> "XHR" -> Refresh webpage (F5)
# -> select "getindex?type..." in "Name" -> "Headers"
# -> "General" -> "Request URL" -> done.

user_name = 'JuJingyi'

#num_page = 90  # The number of pages for crawling (int).
num_page = 3

# Note:
# There are 11 Weibo posts on one page.
# Set "num_page" >> total posts/11.
# Example for Ju Jingyi, "num_page" >> 808/11.


## Part 2 Obtain the list of "cards" information on each page.

ii = 0  # Serial number of pages.
list_cards = []  # Store "cards" information.
while ii < num_page:
    ii = ii + 1
    print('Start crawling all "cards" on page %d.' % ii)
    url = user_url + '&page=' + str(ii)  
    
    response = requests.get(url, headers=headers)
    ob_json = json.loads(response.text)  
    # ob_json (dict)
    
    list_cards.append(ob_json['data']['cards'])  
    # ob_json['data']['cards'] (list)
    
    print('Finish crawling all "cards" on page ' + str(ii) + '.')
    
    print('Suspend 3 seconds.' + '\n' + 30 * '-' + '\n')
    time.sleep(3)
    # Suspend 3 seconds after crawling cards on one page.
    # This avoids failing to download images!!!


## Part 3 Crawl Weibo data (posted text, images and videos).

print(40 * '=' + '\n' + 'The number of pages for crawling is: ' + str(len(list_cards)) + '.' + '\n' + 40 * '=' + '\n')

count_weibo = 1  # Serial number of cards.
page_weibo = 1  # Serial number of pages.

path = user_name + '_Weibo_TI/'
# Path for saving all Weibo data.
# Note: The path should be empty before crawling!!!

for cards in list_cards:
    for card in cards:
        
        print('Start crawling the ' + str(count_weibo) + '-th post on ' + str(page_weibo) + '-th page.')
        
        if card['card_type'] == 9:
            mid = card['mblog']['id']
            created_at = card['mblog']['created_at']  # This is the published time of Weibo post.
            
            # 1/2 Save text of posts.
            if card['mblog']['isLongText'] == 'False':  # Note: 'False' != 'false'.
                text = card['mblog']['text']
            else:
                tmp_url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                tmp_response = requests.get(tmp_url, headers=headers)
                ob_json = json.loads(tmp_response.text)  # ob_json (dict)
                text = ob_json['data']['longTextContent']
                tree = html.fromstring(text)
                text = tree.xpath('string(.)')
            with open(path + user_name + '_Weibo_TIData.txt', 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_weibo) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')
            
            # 2/2 Save imgae of posts.
            if 'bmiddle_pic' in card['mblog']:
                image_path = path + str(count_weibo)
                os.mkdir(image_path)
                url_extend = 'https://m.weibo.cn/status/' + mid  # URL of one Weibo.
                res = requests.get(url_extend, headers=headers).text  # (string)
                imgurl_weibo = re.findall('https://.*large.*.jpg', res)  # Match URL of image.
                x = 1
                for i in range(len(imgurl_weibo)):
                    temp = image_path + '/' + str(x) + '.jpg'
                    # Add image URL to text file.
                    with open(path + user_name + '_Weibo_TIData.txt', 'a', encoding='utf-8') as ff:
                        ff.write('The link of image is：' + imgurl_weibo[i] + '\n')
                    print('Download the %s-th image of this weibo.' % x)
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imgurl_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download this image: %s" % imgurl_weibo[i])
                    x += 1
        
        print('Finish crawling the ' + str(count_weibo) + '-th Weibo post.')
        count_weibo = count_weibo + 1
        
        print('Suspend 3 seconds.\n')  
        time.sleep(3)
        # Suspend 3 seconds after crawling one Weibo post.
        # This avoids failing to download images!!!
    
    print('Finish crawling Weibo data on ' + str(page_weibo) + '-th page.' + '\n' + 40 * '-' + '\n')
    page_weibo = page_weibo + 1
