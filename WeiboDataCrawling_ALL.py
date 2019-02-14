## Task description:
## Crawl Weibo data (posted text, jpg/gif images and videos) of one Weibo user.
## Example: Ju Jingyi (https://m.weibo.cn/u/3669102477).

## Requirement: Python 3.0+.


from lxml import html
import requests
import json
import re
import os
import time
import urllib.request


## Settings.
# Line 27 --- 'Cookie'
# Line 29 --- 'Referer'
# Line 52 --- user_url
# Line 61 --- tmp_folder_time
# Line 62 --- user_name
# Line 65 --- num_page


## Part 1 Set request headers of webpage.

headers = {
'Cookie': 'XXXXXXXXXXXXXX',
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
# Note:  'Cookie' is required for downloading some of videos!!!

user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'

# The information of "user_url" can be obtained as below:
# -> DevTools (F12) -> "XHR" -> Refresh webpage (F5)
# -> select "getindex?type..." in "Name" -> "Headers"
# -> "General" -> "Request URL" -> done.

tmp_folder_name = 'WeiboData_'

tmp_folder_time = '20190119_'
user_name = 'JuJingyi'

#num_page = 90  # The number of pages for crawling (int).
num_page = 90

# Note:
# There are 11 Weibo posts on one page.
# Set "num_page" >> total posts/11.
# Example for Ju Jingyi, "num_page" >> 808/11.

print('\n')
print('Start Weibo data crawling of user - %s.' % user_name)
print('Total pages - %d.' % num_page)
print('\n')

## Part 2 Obtain the list of "cards" information on each page.

ii = 0  # Serial number of pages.
list_cards = []  # Store "cards" information.
while ii < num_page:
    ii += 1
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

path = tmp_folder_name + tmp_folder_time + user_name + '/'
# Path for saving all Weibo data.
# Note: The path should be empty before crawling!!!
os.mkdir(path)

for cards in list_cards:
    for card in cards:
        
        print('Start crawling the ' + str(count_weibo) + '-th post on ' + str(page_weibo) + '-th page.')
        
        if card['card_type'] == 9:
            mid = card['mblog']['id']
            created_at = card['mblog']['created_at']  # This is the published time of Weibo post.
            
            # 1/3 Save text of posts.
            if card['mblog']['isLongText'] == 'False':  # Note: 'False' != 'false'.
                text = card['mblog']['text']
#             else:
#                 tmp_url = 'https://m.weibo.cn/statuses/extend?id=' + mid
#                 tmp_response = requests.get(tmp_url, headers=headers)
#                 ob_json = json.loads(tmp_response.text)  # ob_json (dict)
#                 text = ob_json['data']['longTextContent']
#                 tree = html.fromstring(text)
#                 text = tree.xpath('string(.)')
            else:
                try:
                    tmp_url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                    tmp_response = requests.get(tmp_url, headers=headers)
                    ob_json = json.loads(tmp_response.text)  # ob_json (dict)
                    text = ob_json['data']['longTextContent']
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')
                except:
                    text = "No short text extracted!"
            with open(path + user_name + '_Weibo_ALLData.txt', 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_weibo) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')
            
            # 2/3 Save jpg and gif imgae of original and transferred posts.
            if 'bmiddle_pic' in card['mblog']:
                tag_post = 1  # 1 - original post.
            else:
                tag_post = 2  # 2 - transferred post.
            if (tag_post == 1) | (tag_post == 2):  # Save all post!!!
                image_path = path + str(count_weibo)
                os.mkdir(image_path)
                url_extend = 'https://m.weibo.cn/status/' + mid  # URL of one Weibo.
                res = requests.get(url_extend, headers=headers).text  # (string)
                
                imgjpg_url_weibo = re.findall('https://.*large.*.jpg', res)  # Match URL of jpg image (string).
                imggif_url_weibo = re.findall('https://.*large.*.gif', res)  # Match URL of gif image (string).
                
                # 2-1/3 Save jpg images.
                x_jpg = 1
                for i in range(len(imgjpg_url_weibo)):
                    temp = image_path + '/' + str(x_jpg) + '.jpg'
                    # Add jpg image URL to text file.
                    with open(path + user_name + '_Weibo_ALLData.txt', 'a', encoding='utf-8') as ff:
                        ff.write('The link of image is：' + imgjpg_url_weibo[i] + '\n')
                    print('Download the %s-th image of this weibo.' % x_jpg)
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imgjpg_url_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download this image: %s" % imgjpg_url_weibo[i])
                    x_jpg += 1
                
                # 2-2/3 Save gif images.
                x_gif = 1
                for i in range(len(imggif_url_weibo)):
                    temp = image_path + '/' + str(x_gif) + '.gif'
                    # Add gif image URL to text file.
                    with open(path + user_name + '_Weibo_ALLData.txt', 'a', encoding='utf-8') as ff:
                        ff.write('The link of image is：' + imggif_url_weibo[i] + '\n')
                    print('Download the %s-th image of this weibo.' % x_gif)
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imggif_url_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download this image: %s" % imggif_url_weibo[i])
                    x_gif += 1
                    
            # 3/3 Save video of posts.
            if 'page_info' in card['mblog']:
                if 'media_info' in card['mblog']['page_info']:
                    # Note: Filter Weibo posts with no video that has 'page_info' index!!!
                    
                    video_path = path + str(count_weibo) + '_video'
                    os.mkdir(video_path)

                    videourl_weibo = card['mblog']['page_info']['media_info']['mp4_sd_url']  # (string)
                    # Note: This code obtains the URL of video!!!
                    # Note: The index is manually obtained from DevTools. :p

                    temp = video_path + '/' + str(1) + '.mp4'
                    print('Download the video of this weibo.')  # Each Weibo post has only one video!
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(videourl_weibo).geturl(), temp)
                    except:
                        print("Failed to download this video.")
        
        print('Finish crawling the ' + str(count_weibo) + '-th Weibo post.')
        count_weibo = count_weibo + 1
        
        print('Suspend 5 seconds.\n')  
        time.sleep(5)
        # Suspend 5 seconds after crawling one Weibo post.
        # This avoids failing to download images!!!
    
    print('Finish crawling Weibo data on ' + str(page_weibo) + '-th page.' + '\n' + 40 * '-' + '\n')
    page_weibo = page_weibo + 1
