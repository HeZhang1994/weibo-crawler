# Function: Crawl Weibo data (posted/re-tweeted text, JPG/GIF images, and videos) of one user.

# Requirement: Python 3.0+.

import json
import os
import re
import shutil
import time
import urllib.request

import requests
from lxml import html


# 1. Specify user settings.

WEBSITE_HEADERS = {
    'Cookie': 'XXXXXXXXXXXXXXXXX',
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/3261134763',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
# The information of 'WEBSITE_HEADERS' can be obtained as below:
#     -> DevTools (F12) -> "XHR" -> Refresh web page (F5)
#     -> select "* getindex?type..." in "Name" -> "Headers"
#     -> "Request Headers" -> ... -> done.
# Note:
#     The 'Cookie' is obtained from https://m.weibo.cn/u/3669102477 (login required).
#     The 'Cookie' might be changed in hours and should be updated accordingly.
#     The 'Referer' should be changed for different Weibo user.
# Question:
#     Why the code still can crawl data if the 'Cookie' is set as 'XXX...XXX'?
# Answer:
#     This setting only allows to crawl data that can be accessed by visitor (non-login).
#     To crawl videos and comments, the 'Cookie' is required (login).
#     It is strongly recommended to use the valid 'Cookie' to avoid unknown problems.

USER_URL = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=3261134763&containerid=1076033261134763'
# The information of 'USER_URL' can be obtained as below:
#     -> DevTools (F12) -> "XHR" -> Refresh web page (F5)
#     -> select "* getindex?type..." in "Name" -> "Headers"
#     -> "General" -> "Request URL" -> done.

USER_NAME = 'LYF'

print('\n' + 40 * '=' + '\n' + 'Crawling Weibo data of user - ' + USER_NAME + '\n' + 40 * '=' + '\n')

PAGE_AMOUNT = 1  # The amount of web pages for crawling.
# Note:
#     The number of posts on one web page is 11.
#     The 'PAGE_AMOUNT' is set to be greater than total posts/11.

NAME_FOLDER = 'WeiboData_'
NAME_FILE_TEXT = '_Weibo_PostRecords.txt'


# 2. Create the folders/files for saving data.

# Create a folder for saving data.
PATH_FOLDER = NAME_FOLDER + USER_NAME + '/'

# Create a TEXT file for saving data.
PATH_FILE_TEXT = PATH_FOLDER + USER_NAME + NAME_FILE_TEXT

# Create the folder for saving data.
# Check if the folder exists. If so, delete it and its contents.
if os.path.exists(PATH_FOLDER):
    shutil.rmtree(PATH_FOLDER)
os.mkdir(PATH_FOLDER)


# 3. Request 'cards' information from web pages.

print('\n' + 40 * '-' + '\n' + 'Step 1 - Crawl \'cards\' on web pages' + '\n' + 40 * '-' + '\n')

ii_page = 0  # The serial number of web pages.
list_cards = []  # Record 'cards' information.

while ii_page < PAGE_AMOUNT:
    ii_page += 1
    print('Start crawling \'cards\' on page %d/%d.' % (ii_page, PAGE_AMOUNT))

    url = USER_URL + "&page=" + str(ii_page)
    response = requests.get(url, headers=WEBSITE_HEADERS)
    ob_json = json.loads(response.text)  # ob_json <'dict'>
    list_cards.append(ob_json['data']['cards'])  # ob_json['data']['cards'] <'list'>

    print('Complete!\n')
    time.sleep(3)  # Suspend * seconds after requesting 'cards' information from one page.


# 4. Crawl Weibo data (posted/re-tweeted text, JPG/GIF images and videos).

print('\n' + 40 * '-' + '\n' + 'Step 2 - Crawl Weibo data on web pages' + '\n' + 40 * '-' + '\n')

count_card = 0  # The serial number of cards/posts.
count_page = 0  # The serial number of pages.

for cards in list_cards:
    count_page += 1

    for card in cards:
        count_card += 1
        print('Start crawling the ' + str(count_card) + '-th Weibo post on ' + str(count_page) + '-th page.')

        if card['card_type'] == 9:
            mid = card['mblog']['id']
            created_at = card['mblog']['created_at']  # The published time of current post.

            # 4.1 Crawl text.
            if card['mblog']['isLongText'] == 'False':
                # Note: The content is 'False' rather than 'false'.
                text = card['mblog']['text']
            else:
                try:
                    url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                    response = requests.get(url, headers=WEBSITE_HEADERS)
                    ob_json = json.loads(response.text)  # 'ob_json' <dict>
                    text = ob_json['data']['longTextContent']
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')
                except:
                    text = '***Failed to extract short text from Weibo post.'

            # Save text.
            with open(PATH_FILE_TEXT, 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(count_card) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')

            # 4.2 Crawl JPG/GIF images.
            if 'bmiddle_pic' in card['mblog']:
                tag_post = 1  # Original posts.
            else:
                tag_post = 2  # Re-tweeted posts.

            # Save JPG/GIF images.
            if (tag_post == 1) or (tag_post == 2):
                # Create a child folder for saving JPG/GIF images of current post.
                path_image = PATH_FOLDER + str(count_card)
                os.mkdir(path_image)

                url = 'https://m.weibo.cn/status/' + mid  # The URL of current post.
                res = requests.get(url, headers=WEBSITE_HEADERS).text  # 'res' <str>

                # Find the URL of all large JPG/GIF images.
                image_jpg_urls = re.findall('https://.*large.*.jpg', res)  # 'image_jpg_urls' <list>
                image_gif_urls = re.findall('https://.*large.*.gif', res)  # 'image_gif_urls' <list>

                # 4.2.1 Crawl JPG images.
                count_jpg = 0  # The serial number of JPG images.

                for i in range(len(image_jpg_urls)):
                    if i > 0:
                        # Note: The first URL is not used for downloading image (repeated URL).
                        count_jpg += 1

                        # Add JPG image URL to TEXT file.
                        with open(PATH_FILE_TEXT, 'a', encoding='utf-8') as ff:
                            ff.write('The link of the image is：' + image_jpg_urls[i] + '\n')

                        # Download JPG image.
                        name_image = path_image + '/' + str(count_jpg) + '.jpg'
                        try:
                            print('Download the %s-th JPG image from Weibo post.' % count_jpg)
                            urllib.request.urlretrieve(urllib.request.urlopen(image_jpg_urls[i]).geturl(), name_image)
                        except:
                            print('***Failed to download the JPG image from Weibo post: %s' % image_jpg_urls[i])

                # 4.2.2 Crawl GIF images.
                count_gif = 0  # The serial number of GIF image.

                for i in range(len(image_gif_urls)):
                    if i > 0:
                        # Note: The first URL is not used for downloading image (repeated URL).
                        count_gif += 1

                        # Add GIF image URL to TEXT file.
                        with open(PATH_FILE_TEXT, 'a', encoding='utf-8') as ff:
                            ff.write('The link of the image is：' + image_gif_urls[i] + '\n')

                        # Download GIF image.
                        name_image = path_image + '/' + str(count_gif) + '.gif'
                        try:
                            print('Download the %s-th GIF image from Weibo post.' % count_gif)
                            urllib.request.urlretrieve(urllib.request.urlopen(image_gif_urls[i]).geturl(), name_image)
                        except:
                            print('***Failed to download the GIF image from Weibo post: %s' % image_gif_urls[i])

            # 4.3 Crawl videos.
            if 'page_info' in card['mblog']:
                if 'media_info' in card['mblog']['page_info']:
                    # Note:
                    #     Only video post has '['page_info']['media_info']'.
                    #     Each video post has one video and no image.

                    # Create a child folder for saving the video of current post.
                    path_video = PATH_FOLDER + str(count_card) + '_video'
                    os.mkdir(path_video)

                    # Delete the folder for saving images of current post.
                    # Check if the folder is empty. If so, delete it.
                    if not os.listdir(path_image):
                        os.rmdir(path_image)

                    video_url = card['mblog']['page_info']['media_info']['mp4_sd_url']  # 'video_url' <str>
                    # Note:
                    #     The code returns the video URL of current post.
                    #     The index of 'card' is parsed from DevTools.

                    # Download video.
                    name_video = path_video + '/' + str(1) + '.mp4'
                    try:
                        print('Download the video from Weibo post.')
                        urllib.request.urlretrieve(urllib.request.urlopen(video_url).geturl(), name_video)
                    except:
                        print('***Failed to download the video from Weibo post.')

        print('Complete!\n')
        time.sleep(3)  # Suspend * seconds after crawling data from current post.

    print('Complete crawling Weibo data on ' + str(count_page) + '-th page!' + '\n\n' + 40 * '-' + '\n')
