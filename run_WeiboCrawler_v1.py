'''Function (Python3): Crawl Sina Weibo data (text, JPG/GIF images, and videos) of one Weibo user.

Author: He Zhang @ University of Exeter
Date: April 17th 2019 (Update: April 17th 2019)
Contact: hz298@exeter.ac.uk zhangheupc@126.com

Copyright (c) 2019 He Zhang
'''

import json
import os
import re
import shutil
import time
import urllib.request

import requests
from lxml import html


# 1. Specify settings.

# 1.1 Set the request header (important).
WEBSITE_HEADERS = {
    'Cookie': 'XXXXXXXXXX',
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/3669102477',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
}
# The information of 'WEBSITE_HEADERS' can be obtained as below:
#     -> DevTools (F12) -> 'XHR' -> Refresh web page (F5)
#     -> select '* getindex?type...' in 'Name' -> 'Headers'
#     -> 'Request Headers' -> ... -> done.
# Note:
#     The 'Cookie' can be obtained after user login (required).
#     The 'Cookie' might be changed in hours and should be updated accordingly.
#     The 'Referer' should be changed for crawling Weibo data of different user.
#     The 'User-Agent' should be changed for different environment.
# Question:
#     Why the code still can crawl data if the 'Cookie' is set as 'XXX...XXX'?
# Answer:
#     Setting 'Cookie' as 'XXX...XXX' only allows to crawl data that can be accessed by visitor (non-login).
#     To crawl videos and comments, the valid 'Cookie' is required (login).
#     It is strongly recommended to use the valid 'Cookie' to avoid unknown problems.

# 1.2 Set the request URL of Weibo user (important).
USER_URL = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'
# The information of 'USER_URL' can be obtained as below:
#     -> DevTools (F12) -> 'XHR' -> Refresh web page (F5)
#     -> select '* getindex?type...' in 'Name' -> 'Headers'
#     -> 'General' -> 'Request URL' -> done.

# 1.3 Set the amount of web pages for crawling (important).
PAGE_AMOUNT = 2
# Note:
#     The number of Weibo posts on the first web page is 13.
#     The number of Weibo posts on the other web page is 10.
#     The 'PAGE_AMOUNT' should be greater than 10% of the amount of Weibo posts.

# 1.4 Set the nickname of Weibo user.
USER_NAME = 'JJY'

# 1.5 Set the name of folder/file for saving Weibo data.
NAME_FOLDER = '_WeiboData_v1/'
NAME_FILE_TXT = '_WeiboPost_Records.txt'

print('\n' + 40 * '=' + '\n' + 'Crawling Weibo data of user - ' + USER_NAME + '\n' + 40 * '=' + '\n')


# 2. Create the path for saving Weibo data.

# 2.1 Create the folder for saving Weibo data.
PATH_FOLDER = USER_NAME + NAME_FOLDER

# Check if the folder exists. If so, delete it and create a new one.
if os.path.exists(PATH_FOLDER):
    shutil.rmtree(PATH_FOLDER)
os.mkdir(PATH_FOLDER)

# 2.2 Create the TXT file for recording Weibo data.
PATH_FILE_TXT = PATH_FOLDER + USER_NAME + NAME_FILE_TXT


# 3. Request 'cards' information from web pages.

print('\n' + 40 * '-' + '\n' + 'Step 1 - Crawl \'cards\' information' + '\n' + 40 * '-' + '\n')

ii_page = 0  # The serial number of web pages (starts from '1').
cards_list = []  # The 'cards' of all web pages.

while ii_page < PAGE_AMOUNT:
    ii_page += 1
    print('Start crawling \'cards\' on page %d/%d.' % (ii_page, PAGE_AMOUNT))

    url = USER_URL + '&page=' + str(ii_page)
    response = requests.get(url, headers=WEBSITE_HEADERS)
    obj_json = json.loads(response.text)

    cards_list.append(obj_json['data']['cards'])  # obj_json['data']['cards'] <list>

    time.sleep(3)  # Suspend 3 seconds after requesting 'cards' from current web page.
    print('Complete!\n')


# 4. Crawl Weibo data (original/retweeted text, JPG/GIF images, and videos).

print('\n' + 40 * '-' + '\n' + 'Step 2 - Crawl Weibo data' + '\n' + 40 * '-' + '\n')

count_card = 0  # The serial number of cards/posts on one web page (starts from '1').
count_page = 0  # The serial number of web pages (starts from '1').

for cards in cards_list:
    count_page += 1

    for card in cards:
        count_card += 1
        print('Start crawling the data of ' + str(count_card) + '-th Weibo post on the ' + str(count_page) + '-th page.')

        if card['card_type'] == 9:  # The Weibo post with 'card_type=9' has target data.
            mid = card['mblog']['id']
            created_time = card['mblog']['created_at']  # The published time of current Weibo post.

            # 4.1 Crawl text of Weibo post.
            if card['mblog']['isLongText'] == 'False':  # The string is 'False' not 'false'.
                text = card['mblog']['text']
            else:
                try:
                    url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                    response = requests.get(url, headers=WEBSITE_HEADERS)
                    obj_json = json.loads(response.text)
                    text = obj_json['data']['longTextContent']
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')
                except:
                    print('*****Error: Failed to extract text.')
                    text = '*****Error: Failed to extract text.'

            # Add text to TXT file.
            with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_card) + '-th Weibo\n' + '***  Published on  ' + created_time + '  ***' + '\n')
                ff.write(text + '\n')

            # 4.2 Crawl JPG/GIF images.
            if 'bmiddle_pic' in card['mblog']:
                tag_post = 1  # The original Weibo post.
            else:
                tag_post = 2  # The retweeted Weibo post.

            # Crawl JPG/GIF images of current Weibo post (original/retweeted).
            if (tag_post == 1) or (tag_post == 2):
                # Create a sub-folder for saving JPG/GIF images.
                path_image = PATH_FOLDER + str(count_card) + '/'
                os.mkdir(path_image)

                url = 'https://m.weibo.cn/status/' + mid  # The request URL of current Weibo post.
                res = requests.get(url, headers=WEBSITE_HEADERS).text  # 'res' <str>

                # Find the URL of all large JPG/GIF images.
                # Note: 'large' can be replaced by 'orj360' for finding small images.
                image_jpg_urls = re.findall('https://.*large.*.jpg', res)  # 'image_jpg_urls' <list>
                image_gif_urls = re.findall('https://.*large.*.gif', res)  # 'image_gif_urls' <list>

                # 4.2.1 Crawl JPG images.
                for i in range(len(image_jpg_urls)):
                    # The first URL (i = 0, repeated) is not used for downloading image.
                    if i > 0:
                        # Add JPG image URL to TXT file.
                        with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                            ff.write('The link of the JPG image is：' + image_jpg_urls[i] + '\n')

                        # Download and save JPG image.
                        name_image = path_image + str(i) + '.jpg'
                        try:
                            print('Download the %s-th JPG image.' % i)
                            urllib.request.urlretrieve(urllib.request.urlopen(image_jpg_urls[i]).geturl(), name_image)
                            time.sleep(1)
                        except:
                            print('*****Error: Failed to download the JPG image: %s' % image_jpg_urls[i])
                            # Add download error information to TXT file.
                            with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                                ff.write('*****Error: Failed to download the JPG image：' + image_jpg_urls[i] + '\n')

                # 4.2.2 Crawl GIF images.
                for i in range(len(image_gif_urls)):
                    # The first URL (i = 0, repeated) is not used for downloading image.
                    if i > 0:
                        # Add GIF image URL to TXT file.
                        with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                            ff.write('The link of the GIF image is：' + image_gif_urls[i] + '\n')

                        # Download and save GIF image.
                        name_image = path_image + str(i) + '.gif'
                        try:
                            print('Download the %s-th GIF image.' % i)
                            urllib.request.urlretrieve(urllib.request.urlopen(image_gif_urls[i]).geturl(), name_image)
                            time.sleep(1)
                        except:
                            print('*****Error: Failed to download the GIF image: %s' % image_gif_urls[i])
                            # Add download error information to TXT file.
                            with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                                ff.write('*****Error: Failed to download the GIF image：' + image_gif_urls[i] + '\n')

            # 4.3 Crawl video.
            # Create a sub-folder for saving video.
            path_video = PATH_FOLDER + str(count_card) + '_video/'
            os.mkdir(path_video)

            # 4.3.1 Crawl the video of current Weibo post (original).
            if 'retweeted_status' not in card['mblog']:
                # Note:
                #     Only video post (original) has '['page_info']['media_info']'.
                #     Only video post (non-live) has '...['mp4_sd_url']'.
                #     Each video post only has one video.
                if 'page_info' in card['mblog']:
                    if 'media_info' in card['mblog']['page_info']:
                        if 'mp4_sd_url' in card['mblog']['page_info']['media_info']:
                            # Add video information to TXT file.
                            with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                                ff.write('This original Weibo post has video.' + '\n')

                            # Get the download URL of video.
                            # Note:
                            #     The code returns the video URL of current Weibo post.
                            #     The index of 'card[...]...' can be parsed from DevTools (F12).
                            video_url = card['mblog']['page_info']['media_info']['mp4_sd_url']

                            # Download and save video.
                            name_video = path_video + str(1) + '.mp4'  # 'str(1)' - 'only has one video'.
                            try:
                                print('Download the video (original).')
                                urllib.request.urlretrieve(urllib.request.urlopen(video_url).geturl(), name_video)
                                time.sleep(1)
                            except:
                                print('*****Error: Failed to download the video (original).')
                                # Add download error information to TXT file.
                                with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                                    ff.write('*****Error: Failed to download the video (original).' + '\n')

            # 4.3.2 Crawl the video of current Weibo post (retweeted).
            if 'retweeted_status' in card['mblog']:
                # Note:
                #     Only video post (retweeted) has '['retweeted_status']['page_info']['media_info']'.
                #     Only video post (non-live) has '...['mp4_sd_url']'.
                #     Each video post only has one video.
                if 'page_info' in card['mblog']['retweeted_status']:
                    if 'media_info' in card['mblog']['retweeted_status']['page_info']:
                        if 'mp4_sd_url' in card['mblog']['retweeted_status']['page_info']['media_info']:
                            # Add video information to TXT file.
                            with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                                ff.write('This retweeted Weibo post has video.' + '\n')

                            # Get the download URL of video.
                            # Note:
                            #     The code returns the video URL of current Weibo post.
                            #     The index of 'card[...]...' can be parsed from DevTools (F12).
                            video_url = card['mblog']['retweeted_status']['page_info']['media_info']['mp4_sd_url']

                            # Download and save video.
                            name_video = path_video + str(1) + '.mp4'  # 'str(1)' - 'only has one video'.
                            try:
                                print('Download the video (retweeted).')
                                urllib.request.urlretrieve(urllib.request.urlopen(video_url).geturl(), name_video)
                                time.sleep(1)
                            except:
                                print('*****Error: Failed to download the video (retweeted).')
                                # Add download error information to TXT file.
                                with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                                    ff.write('*****Error: Failed to download the video (retweeted).' + '\n')

        # 5.1 Check if the sub-folder for saving JPG/GIF images is empty. If so, delete it.
        if os.path.exists(path_image):
            if not os.listdir(path_image):
                os.rmdir(path_image)

        # 5.2 Check if the sub-folder for saving video is empty. If so, delete it.
        if os.path.exists(path_video):
            if not os.listdir(path_video):
                os.rmdir(path_video)

        time.sleep(3)  # Suspend 3 seconds after crawling Weibo data from current Weibo post.
        print('Complete!\n')

    print('Complete crawling Weibo data on ' + str(count_page) + '-th page!' + '\n\n' + 40 * '-' + '\n')
