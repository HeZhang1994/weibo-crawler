### Function: Crawl Weibo data (posted/re-tweeted text, JPG/GIF images and videos) of one Weibo user (e.g., JJY).

# Requirement: Python 3.0+.

import os
import shutil
import requests
import json
from lxml import html
import time
import re
import urllib.request


## Part 1 - Specify user settings.

# Line  --- 'Cookie'
# Line  --- 'Referer'
# Line  --- 'user_url'
# Line  --- 'tmp_folder_name'
# Line  --- 'tmp_folder_time'
# Line  --- 'user_name'
# Line  --- 'num_page'

# User settings.
headers = {
'Cookie': '_T_WM=38dc7eab658e056d17f4b0c13c49e4ee; ALF=1552522335; SCF=Al40pEkgsi84UdpvySnR_2wwcSK7oXDzNBTm9kKAMcnPdJ5ARB1RSmZwedRviX6t4pjHxGYC1t9HMMG9e57Og_U.; SUB=_2A25xZn8wDeRhGeBH7FcV8yzPzD6IHXVSqQF4rDV6PUNbktBeLUPdkW1NQaUxHGBAD-3rQJsWOwwvM9Pe9umznn4Z; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5_ndb4SLZwPI5jAxklZgCc5JpX5KMhUgL.Foq4S0-Xe0z0S0z2dJLoI0YLxKMLB.zL1K.LxKqL1hnL1K2LxK-LB.eLBK5LxKMLB.2LBonLxK.L1--LBK5LxK-LBK.LBKMLxKMLBK-L12-t; SUHB=010GUgFNPcqf-_; MLOGIN=1; XSRF-TOKEN=a512af; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076033669102477%26fid%3D1005053669102477%26uicode%3D10000011',
'Host': 'm.weibo.cn',
'Referer': 'https://m.weibo.cn/u/3669102477',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
# The information of 'headers' can be obtained as below:
#     -> DevTools (F12) -> "XHR" -> Refresh web page (F5)
#     -> select "* getindex?type..." in "Name" -> "Headers"
#     -> "Request Headers" -> ... -> done.
# Note:
#     The 'Cookie' is obtained from https://m.weibo.cn/u/3669102477 (login required).
#     The 'Cookie' might be changed in hours and should be updated accordingly.
#     The 'Referer' should be changed for different Weibo user.
# Question:
#     Why the code still can crawl Weibo data if the 'Cookie' is set as 'XXX...XXX'?
# Answer:
#     This setting only allows to crawl Weibo data that can be accessed by visitor (non-login).
#     To crawl videos and comments, the 'Cookie' is required (login).
#     It is strongly recommended to use the valid 'Cookie' to avoid unknown problems.

# User settings.
user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'
# The information of 'user_url' can be obtained as below:
#     -> DevTools (F12) -> "XHR" -> Refresh web page (F5)
#     -> select "* getindex?type..." in "Name" -> "Headers"
#     -> "General" -> "Request URL" -> done.

# User settings.
tmp_folder_name = 'WeiboData_'
tmp_folder_time = '2019_'
user_name = 'JJY'

txt_file_name = '_Weibo_DataRecords.txt'

# User settings.
num_page = 1  # The number of crawling pages.
# Note:
#     There are 11 Weibo posts per page.
#     Set 'num_page' ~ total posts/11.

# Create the path/folder for saving Weibo data.
path = tmp_folder_name + tmp_folder_time + user_name + '/'
if os.path.exists(path) is True:  # Check if the path/folder exists.
    shutil.rmtree(path)  # Delete the folder, its child folders and child files.
os.mkdir(path)  # Create a new folder.

print('\n' + 40 * '=' + '\n' + 'Crawling Weibo data of user - ' + user_name + '.\n' + 40 * '=')


## Part 2 - Request "cards" information from web pages.

print('\n' + 40 * '=' + '\n' + 'The number of crawling pages is: ' + str(num_page) + '.' + '\n' + 40 * '=' + '\n')

ii = 0  # The serial number of web pages.
list_cards = []  # Record "cards" information.

while ii < num_page:
    ii += 1
    print('Start crawling "cards" on page %d/%d.' % (ii, num_page))
    
    url = user_url + '&page=' + str(ii)
    response = requests.get(url, headers=headers)
    ob_json = json.loads(response.text)  # ob_json <'dict'>
    list_cards.append(ob_json['data']['cards'])  # ob_json['data']['cards'] <'list'>
    
    time.sleep(3)  # Suspend * seconds after requesting "cards" information from one page.
    print('Complete!')


## Part 3 - Crawl Weibo data (posted/re-tweeted text, JPG/GIF images and videos).

print('\n' + 40 * '=' + '\n' + 'The number of crawling pages is: ' + str(len(list_cards)) + '.' + '\n' + 40 * '=' + '\n')

count_weibo = 0  # The serial number of cards.
page_weibo = 0  # The serial number of pages.

for cards in list_cards:
    page_weibo += 1
    
    for card in cards:
        count_weibo += 1
        print('Start crawling the ' + str(count_weibo) + '-th post on ' + str(page_weibo) + '-th page.')
        
        if card['card_type'] == 9:
            mid = card['mblog']['id']
            created_at = card['mblog']['created_at']  # The posted time.
            
            # 1/3 Crawl text.
            if card['mblog']['isLongText'] == 'False':  # Note: 'False' != 'false'.
                text = card['mblog']['text']
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
            
            # Save text.
            with open(path + user_name + txt_file_name, 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_weibo) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')
            
            # 2/3 Crawl JPG/GIF images.
            if 'bmiddle_pic' in card['mblog']:
                tag_post = 1  # 1 - original post.
            else:
                tag_post = 2  # 2 - re-tweeted post.
            
            if (tag_post == 1) or (tag_post == 2):  # Save all post.
                # Create a child folder for saving images.
                image_path = path + str(count_weibo)
                os.mkdir(image_path)
                
                url_extend = 'https://m.weibo.cn/status/' + mid  # URL of one Weibo.
                res = requests.get(url_extend, headers=headers).text  # <'string'>
                
                imgjpg_url_weibo = re.findall('https://.*large.*.jpg', res)  # Match URL of JPG images <'string'>.
                imggif_url_weibo = re.findall('https://.*large.*.gif', res)  # Match URL of GIF images <'string'>.
                
                # 2-1/3 Crawl JPG images.
                x_jpg = 0  # The serial number of JPG image.
                
                for i in range(len(imgjpg_url_weibo)):
                    x_jpg += 1
                    
                    # Add JPG image URL to .txt file.
                    temp = image_path + '/' + str(x_jpg) + '.jpg'
                    with open(path + user_name + txt_file_name, 'a', encoding='utf-8') as ff:
                        ff.write('The link of the image is：' + imgjpg_url_weibo[i] + '\n')
                    print('Download the %s-th image.' % x_jpg)
                    
                    # Download JPG image.
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imgjpg_url_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download the image: %s" % imgjpg_url_weibo[i])
                
                # 2-2/3 Crawl GIF images.
                x_gif = 0  # The serial number of GIF image.
                
                for i in range(len(imggif_url_weibo)):
                    x_gif += 1
                    
                    # Add GIF image URL to .txt file.
                    temp = image_path + '/' + str(x_gif) + '.gif'
                    with open(path + user_name + txt_file_name, 'a', encoding='utf-8') as ff:
                        ff.write('The link of the image is：' + imggif_url_weibo[i] + '\n')
                    print('Download the %s-th image.' % x_gif)
                    
                    # Download GIF image.
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imggif_url_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download the image: %s" % imggif_url_weibo[i])
            
            # 3/3 Crawl videos.
            if 'page_info' in card['mblog']:
                if 'media_info' in card['mblog']['page_info']:  # Filter Weibo posts with video that has 'page_info' index.
                    # Create a child folder for saving video.
                    video_path = path + str(count_weibo) + '_video'
                    os.mkdir(video_path)
                    
                    videourl_weibo = card['mblog']['page_info']['media_info']['mp4_sd_url']  # <'string'>
                    # Note:
                    #     This code obtains the URL of video.
                    #     The index is manually parsed from DevTools.
                    
                    temp = video_path + '/' + str(1) + '.mp4'
                    print('Download the video.')  # Each Weibo post only has one video.
                    
                    # Download video.
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(videourl_weibo).geturl(), temp)
                    except:
                        print("Failed to download the video.")
        
        time.sleep(3)  # Suspend * seconds after crawling data from one Weibo post.
        print('Complete!\n')
    
    print('Complete crawling Weibo data on ' + str(page_weibo) + '-th page!' + '\n\n' + 40 * '-' + '\n')
