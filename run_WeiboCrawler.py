'''Crawl Sina Weibo data (text, JPG/GIF images, live photos, and videos) of one Weibo user.

Author: He Zhang @ University of Exeter
Date: 16th April 2019 (Update: 18th April 2019)
Contact: hz298@exeter.ac.uk zhangheupc@126.com

Copyright (c) 2019 He Zhang
'''

# Python 3.7

import json
import os
import re
import shutil
import time

import requests
from lxml import html

from pyCrawler_function import crawl_image
from pyCrawler_function import crawl_livephoto
from pyCrawler_function import crawl_video


# 1. Specify settings.

# 1.1 Set the request header of Weibo (important).
WEBSITE_HEADERS = {
    'Cookie': '_T_WM=9d806bdcd07d9ad7bb26ae23d94b8553; SCF=AuZmy8W7MgXGJINni_v0fNnE7CAh4QeGplsbaEBVe20UBT8HZ91dqgofOfT1a1fi0OHdLVUy7OW6WGmmE0VQIXA.; SUB=_2A25xsaJzDeRhGeBH7FcV8yzPzD6IHXVTXc47rDV6PUJbkdBeLRbRkW1NQaUxHBnd5-RcycV101Gze6TEe5U_MTn8; SUHB=0pHxkqqBgd6rn7; WEIBOCN_WM=3333_2001; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=0f52ee; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076033669102477%26fid%3D1005053669102477%26uicode%3D10000011',
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
#     The 'Cookie' is obtained after login with an valid account on m.weibo.cn.
#     The 'Cookie' might be changed in hours and should be updated accordingly.
#     The 'Referer' should be changed for crawling Weibo data of different user.
#     The 'User-Agent' should be changed for different environments.
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
PAGE_AMOUNT = 3
# Note:
#     The number of Weibo posts on the first web page is 13.
#     The number of Weibo posts on the other web page is 10.
#     The 'PAGE_AMOUNT' should be greater than 10% of the amount of Weibo posts.

# 1.4 Set the nickname of Weibo user.
USER_NAME = 'JJY'

# 1.5 Create the folder for saving Weibo data.
PATH_FOLDER = USER_NAME + '_WeiboData/'
if os.path.exists(PATH_FOLDER):
    shutil.rmtree(PATH_FOLDER)
os.mkdir(PATH_FOLDER)

# 1.6 Set the TXT file for saving Weibo information.
PATH_FILE_TXT = PATH_FOLDER + USER_NAME + '_WeiboPost_Records.txt'

# 1.7 Select the type of Weibo data for crawling (0 - No, 1 - Yes).
IF_IMAGE = 1
IF_PHOTO = 1
IF_VIDEO = 1
IF_LIVE2GIF = 1  # If crawl live photos as GIF images.

# 2. Request 'cards' information from web pages.

print('\n' + 40 * '=' + '\n' + 'Crawling Weibo data of user - ' + USER_NAME + '\n' + 40 * '=' + '\n')

print('\n' + 40 * '-' + '\n' + 'Step 1 - Crawl \'cards\' Information' + '\n' + 40 * '-' + '\n')

count_page = 0  # The serial number of web pages (starts from '1').
cards_list = []  # The 'cards' of all web pages.

while count_page < PAGE_AMOUNT:
    count_page += 1

    print('Start crawling \'cards\' on page %d/%d.' % (count_page, PAGE_AMOUNT))

    url = USER_URL + '&page=' + str(count_page)
    response = requests.get(url, headers=WEBSITE_HEADERS)
    content = json.loads(response.text)  # <dict>
    cards_list.append(content['data']['cards'])  # content['data']['cards'] <list>

    time.sleep(3)  # Suspend 3 seconds after requesting 'cards' from current web page.
    print('Complete!\n')

# 3. Crawl Weibo data (text, JPG/GIF images, live photos, and videos).

print('\n' + 40 * '-' + '\n' + 'Step 2 - Crawl Weibo Data' + '\n' + 40 * '-' + '\n')

count_page = 0  # The serial number of web pages (starts from '1').
count_card = 0  # The serial number of cards/posts on one web page (starts from '1').

for cards in cards_list:
    count_page += 1

    for card in cards:
        count_card += 1

        print('Start crawling the ' + str(count_card) + '-th Weibo post on page %d/%d.' % (count_page, PAGE_AMOUNT))

        if card['card_type'] == 9:  # The Weibo post with 'card_type = 9' has data.
            mid = card['mblog']['id']
            publish_time = card['mblog']['created_at']

            # 3.1 Crawl text.
            if card['mblog']['isLongText'] == 'False':  # The string is 'False' not 'false'.
                text = card['mblog']['text']
            else:
                try:
                    url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                    response = requests.get(url, headers=WEBSITE_HEADERS)
                    content = json.loads(response.text)
                    text = content['data']['longTextContent']
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')
                except:
                    print('*****Error: Failed to extract text.')
                    text = '*****Error: Failed to extract text.'

            # Save text to TXT file.
            with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_card) + '-th Weibo\n' + '***  Published on ' + publish_time + '  ***' + '\n')
                ff.write(text + '\n')

            # 3.2 Crawl JPG/GIF images.
            if IF_IMAGE == 1:
                # Step 1 Create a sub-folder for saving JPG/GIF images.
                path_image = PATH_FOLDER + str(count_card) + '/'
                os.mkdir(path_image)

                # Step 2 Get the URL of JPG/GIF images.
                image_jpg_urls = []
                image_gif_urls = []
                url = 'https://m.weibo.cn/status/' + mid
                res = requests.get(url, headers=WEBSITE_HEADERS).text  # <str>
                # Find the URL of large images.
                image_jpg_urls = re.findall('https://.*large.*.jpg', res)  # <list>
                image_gif_urls = re.findall('https://.*large.*.gif', res)  # <list>
                # Find the URL of small images if no large image is found.
                if not image_jpg_urls:
                    image_jpg_urls = re.findall('https://.*orj360.*.jpg', res)
                if not image_gif_urls:
                    image_gif_urls = re.findall('https://.*orj360.*.gif', res)

                # Step 3-1 Crawl JPG images.
                if image_jpg_urls:
                    crawl_image(PATH_FILE_TXT, path_image, image_jpg_urls, '.jpg')
                # Step 3-2 Crawl GIF images.
                if image_gif_urls:
                    crawl_image(PATH_FILE_TXT, path_image, image_gif_urls, '.gif')

                # Step 4 Delete the empty sub-folder.
                if os.path.exists(path_image):
                    if not os.listdir(path_image):
                        os.rmdir(path_image)

            # 3.3 Crawl live photos.
            if IF_PHOTO == 1:
                # Step 1 Create a sub-folder for saving live photos.
                path_photo = PATH_FOLDER + str(count_card) + '_livephoto/'
                os.mkdir(path_photo)

                # Step 2 Get the URL of live photos.
                photo_urls = []
                photo_url_start = 'https://video.weibo.com/media/play?livephoto=//us.sinaimg.cn/'  # Fixed.
                photo_url_end = '.mov&KID=unistore,videomovSrc'  # Fixed.
                # Find the URL of live photos in original/retweeted Weibo post.
                if 'retweeted_status' not in card['mblog']:
                    card_info = card['mblog']
                elif 'retweeted_status' in card['mblog']:
                    card_info = card['mblog']['retweeted_status']
                if 'pic_video' in card_info:
                    photo_str = card['mblog']['pic_video']
                    photo_list = re.split('[,]', photo_str)
                    for photo in photo_list:
                        # E.g., 'photo' = '0:000voDMsjx07t57qM583010f0100alDF0k01'
                        photo_code = re.split('[:]', photo)[1]
                        photo_url = photo_url_start + photo_code + photo_url_end
                        photo_urls.append(photo_url)

                # Step 3 Crawl live photos.
                if photo_urls:
                    crawl_livephoto(PATH_FILE_TXT, path_photo, photo_urls, IF_LIVE2GIF)

                # Step 4 Delete the empty sub-folder.
                if os.path.exists(path_photo):
                    if not os.listdir(path_photo):
                        os.rmdir(path_photo)

            # 3.4 Crawl videos.
            if IF_VIDEO == 1:
                # Step 1 Create a sub-folder for saving video.
                path_video = PATH_FOLDER + str(count_card) + '_video/'
                os.mkdir(path_video)

                # Step 2 Get the URL of videos (HD and SD).
                video_url = ''  # Each Weibo post only has one video.
                video_hd_url = ''
                video_sd_url = ''
                card_info = ''
                # Find the URL of video in original/retweeted Weibo post.
                if 'retweeted_status' not in card['mblog']:
                    try:
                        card_info = card['mblog']['page_info']['media_info']
                    except:
                        card_info = ''
                elif 'retweeted_status' in card['mblog']:
                    try:
                        card_info = card['mblog']['retweeted_status']['page_info']['media_info']
                    except:
                        card_info = ''
                if card_info:
                    # Find the URL of HD video.
                    try:
                        video_hd_url = card_info['mp4_hd_url']
                    except:
                        video_hd_url = ''
                    # Find the URL of SD video.
                    try:
                        video_sd_url = card_info['mp4_sd_url']
                    except:
                        video_sd_url = ''
                # HD video is preferred.
                if video_hd_url:
                    video_url = video_hd_url
                elif video_sd_url:
                    video_url = video_sd_url

                # Step 3 Crawl video.
                if video_url:
                    crawl_video(PATH_FILE_TXT, path_video, video_url, '.mp4')

                # Step 4 Delete the empty sub-folder.
                if os.path.exists(path_video):
                    if not os.listdir(path_video):
                        os.rmdir(path_video)

        time.sleep(3)  # Suspend 3 seconds after crawling Weibo data from current Weibo post.
        print('Complete!\n')

    print('Complete crawling Weibo data on ' + str(count_page) + '-th page!' + '\n\n' + 40 * '-' + '\n')
