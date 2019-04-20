'''Crawl Weibo data of one Sina Weibo user.
The Weibo data include: Text, JPG/GIF images, live photos, and videos.
This code simulates login of Sina Weibo by using session (not cookie)!

Author: He Zhang @ University of Exeter
Date: 16th April 2019 (Update: 20th April 2019)
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
from pyCrawler_function import crawl_photo
from pyCrawler_function import crawl_video


# 1. Specify settings.

# 1.1 Simulate login of Sina Weibo by using session (important).
S_URL = r'https://passport.weibo.cn/signin/login'  # Fixed.
S_DATA = {'username': 'XXXXX',  # Replace XXXXX with the username of a valid Sina Weibo account.
          'password': 'YYYYY',  # Replace YYYYY with the password of the account.
          'savestate': '1',
          'r': r'',
          'ec': '0',
          'pagerefer': '',
          'entry': 'mweibo',
          'wentry': '',
          'loginfrom': '',
          'client_id': '',
          'code': '',
          'qq': '',
          'mainpageflag': '1',
          'hff': '',
          'hfp': ''
          }
S_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Host': 'passport.weibo.cn'
            }
session = requests.session()
session.post(url=S_URL, data=S_DATA, headers=S_HEADER)
# The information of 'S_DATA' and 'S_HEADER' can be obtained as below:
#     -> Open 'https://passport.weibo.cn/signin/login' on browser
#     -> Login with a valid Sina Weibo account
#     -> DevTools (F12) -> 'XHR' (tag) -> Refresh web page (F5)
#     -> Open 'login' (file) in 'Name' (tag) -> 'Headers' (tag)
#     -> To obtain 'S_DATA', see 'Form Data'.
#     -> To obtain 'S_HEADER', see 'Request Headers'.

# 1.2 Set the request URL of target Sina Weibo user (important).
USER_URL = r'https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1076033669102477'
# The information of 'USER_URL' can be obtained as below:
#     -> Open 'https://m.weibo.cn/u/3669102477' on browser
#     -> Login with a valid Sina Weibo account
#     -> DevTools (F12) -> 'XHR' (tag) -> Refresh web page (F5)
#     -> Open '*getindex...' (file) in 'Name' (tag) -> 'Headers' (tag)
#     -> To obtain 'USER_URL', see 'General' -> 'Request URL'.
# Note:
#     '3669102477' is the unique ID of the target Sina Weibo user.
#     The ID can be found in the address bar by opening user's homepage on browser. 

# 1.3 Set the amount of web pages for crawling (important).
PAGE_AMOUNT = 3
# Note:
#     The number of Weibo posts on the first web page is 13.
#     The number of Weibo posts on the other web page is 10.
#     The 'PAGE_AMOUNT' should be greater than 10% of the amount of Weibo posts.

# 1.4 Set the nickname of Sina Weibo user.
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
IF_LIVE2GIF = 1  # If convert crawler live photos to GIF images.

# 1.8 Set the time delay of crawler.
TIME_DELAY = 3


# 2. Request 'cards' information from web pages.

print('\n' + 40 * '=' + '\n' + 'Crawling Weibo Data of User - ' + USER_NAME + '\n' + 40 * '=')

count_page = 0  # The serial number of web pages (starts from '1').
count_card = 0  # The serial number of cards/posts on one web page (starts from '1').

while count_page < PAGE_AMOUNT:
    count_page += 1

    print('\n' + 40 * '-' + '\n' + 'Step 1 - Crawl \'cards\' Information' + '\n' + 40 * '-' + '\n')
    print('Start crawling \'cards\' on page %d/%d.' % (count_page, PAGE_AMOUNT))

    cards_list = []  # The 'cards' of all web pages.
    
    url = USER_URL + '&page=' + str(count_page)
    response = session.get(url)
    content = json.loads(response.text)  # <dict>
    cards_list.append(content['data']['cards'])  # content['data']['cards'] <list>

    time.sleep(TIME_DELAY)  # Suspend TIME_DELAY seconds after requesting 'cards' from current web page.
    print('Complete!')

    # 3. Crawl Weibo data on current web page (to avoid 'card' expiration of video posts).

    print('\n' + 40 * '-' + '\n' + 'Step 2 - Crawl Weibo Data of ' + USER_NAME + '\n' + 40 * '-' + '\n')

    for cards in cards_list:
        for card in cards:
            count_card += 1

            print('Start crawling the ' + str(count_card) + '-th Weibo post on page %d/%d.' % (count_page, PAGE_AMOUNT))

            if card['card_type'] == 9:  # The Weibo post with 'card_type = 9' has data.
                mid = card['mblog']['id']
                publish_time = card['mblog']['created_at']

                # 3.1 Crawl short text.
                print('Is LONG text?', card['mblog']['isLongText'])
                if card['mblog']['isLongText'] == 'True':  # The string is 'True' not 'true'.
                    text = '{LongText}'
                elif card['mblog']['isLongText'] == 'False':  # The string is 'False' not 'false'.
                    text = card['mblog']['text']
                else:
                    text = card['mblog']['text']

                # Convert text to normal format (by removing hyperlinks).
                tree = html.fromstring(text)
                text = tree.xpath('string(.)')

                # Save text to TXT file.
                with open(PATH_FILE_TXT, 'a', encoding='utf-8') as ff:
                    ff.write('\n' + 'The ' + str(count_card) + '-th Weibo id: ' + str(mid) + '\n')
                    ff.write('***  Published on ' + publish_time + '  ***' + '\n')
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
                    res = session.get(url).text  # <str>
                    # Find the URL of large JPG/GIF images.
                    image_jpg_urls = re.findall('https://.*large.*.jpg', res)  # <list>
                    image_gif_urls = re.findall('https://.*large.*.gif', res)  # <list>
                    # Find the URL of small JPG/GIF images if no large image is found.
                    if not image_jpg_urls:
                        image_jpg_urls = re.findall('https://.*orj360.*.jpg', res)
                    if not image_gif_urls:
                        image_gif_urls = re.findall('https://.*orj360.*.gif', res)

                    # Step 3 Crawl JPG/GIF images.
                    if image_jpg_urls:
                        crawl_image(PATH_FILE_TXT, path_image, image_jpg_urls, '.jpg')
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
                        crawl_photo(PATH_FILE_TXT, path_photo, photo_urls, if_live2gif=IF_LIVE2GIF)

                    # Step 4 Delete the empty sub-folder.
                    if os.path.exists(path_photo):
                        if not os.listdir(path_photo):
                            os.rmdir(path_photo)

                # 3.4 Crawl videos.
                if IF_VIDEO == 1:
                    # Step 1 Create a sub-folder for saving video.
                    path_video = PATH_FOLDER + str(count_card) + '_video/'
                    os.mkdir(path_video)

                    # Step 2 Get the URL of video (HD and/or SD).
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
                    # HD video is preferred for crawling.
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

            time.sleep(TIME_DELAY)  # Suspend TIME_DELAY seconds after crawling Weibo data from current Weibo post.
            print('Complete!\n')

    print('Complete crawling Weibo data on ' + str(count_page) + '-th page!' + '\n\n' + 40 * '-' + '\n')
