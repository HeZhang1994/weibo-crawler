import os
import re
import shutil
import time
import urllib.request
from subprocess import check_output

import cv2
import imageio
from PIL import Image


def time_str2float(timestamp):
    '''Convert a timestamp to a floating number.

    Parameter:
        timestamp <str> - The input timestamp formatted as 'hh:mm:ss.msec'.

    Return:
        time_num <float> - The number of the input timestamp formatted as 'ss.msec'.
    '''
    time_list = re.split('[:]', timestamp)
    time_num = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + float(time_list[2])

    return time_num


def get_video_duration(path_video):
    '''Get the duration of a video.

    Parameter:
        path_video <str> - The path of the input video.

    Return:
        duration <str> - The duration of the input video formatted as 'hh:mm:ss.msec'.
    '''
    # Create the command for getting the information of the input video via ffprobe.
    cmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', path_video]
    # Get the information of the input video via ffprobe command.
    info_byte = check_output(cmd)  # <bytes>
    # Decode the information.
    info_str = info_byte.decode("utf-8")  # <str>
    # Split the information.
    info_list = re.split('[\n]', info_str)

    # Get the duration of the input video.
    for info in info_list:
        if 'duration' in info:
            # E.g., 'info' = 'duration=0:00:01.860000'.
            duration = re.split('[=]', info)[1]

    return duration


def resize_image(path_image, ratio=0.4):
    '''Resize and overwrite an image.

    Parameters:
        path_image <str> - The path of the input image.
        ratio <float> - The resizing ratio. Default is '0.4'.

    Return:
        0 <int> - If the task is completed.
    '''
    img = Image.open(path_image)
    width, height = img.size
    img = img.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
    img.save(path_image)

    return 0


def create_gif(path_gif, duration_gif, folder_frame, frmt_frame='.jpg'):
    '''Create a GIF image with the given frames.

    Parameters:
        path_gif <str> - The path for saving the output GIF image.
        duration_gif <float> - The duration of the output GIF image.
        folder_frame <str> - The folder of the input frames.
        frmt_frame <str> - The format of the input frames. Default is '.jpg'.

    Return:
        0 <int> - If the task is completed.
    '''
    # Get the name of the input (sorted) frames.
    imgFames = sorted((iN for iN in os.listdir(folder_frame) if iN.endswith(frmt_frame)))
    # Calculate the duration of each frame.
    duration_frame = duration_gif / len(imgFames)

    # Create the output GIF image.
    imgGIF = []
    for imgFame in imgFames:
        # Scale down the size of each frame.
        resize_image(folder_frame + imgFame)
        # Concatenate each frame.
        imgGIF.append(imageio.imread(folder_frame + imgFame))

    # Save the output GIF image.
    imageio.mimsave(path_gif, imgGIF, duration=duration_frame)

    return 0


def video2gif(path_video, folder_gif, name_gif):
    '''Convert a video to a GIF image.

    Parameters:
        path_video <str> - The path of the input video.
        folder_gif <str> - The folder for saving the output GIF image.
        name_gif <str> - The name of the output GIF image.

    Return:
        0 <int> - If the task is completed.
    '''
    # Initialize a temporary folder for saving video frames.
    folder_tmp = folder_gif + 'tmp/'
    if os.path.exists(folder_tmp):
        shutil.rmtree(folder_tmp)
    os.mkdir(folder_tmp)

    # Extract video frames.
    vidcap = cv2.VideoCapture(path_video)  # <cv2.VideoCapture>
    success, image = vidcap.read()  # 'success' <bool>, 'image' <numpy.ndarray>
    count = 0
    while success:
        path = folder_tmp + 'frame_' + str(count).zfill(3) + '.jpg'
        cv2.imwrite(path, image)  # Save each frame as an image (JPG/PNG).
        success, image = vidcap.read()
        count += 1

    # Create the output GIF image.
    duration_str = get_video_duration(path_video)
    duration_num = time_str2float(duration_str)
    create_gif(folder_gif + name_gif, duration_num, folder_tmp)

    # Delete the temporary folder.
    if os.path.exists(folder_tmp):
        shutil.rmtree(folder_tmp)

    return 0


def crawl_image(txt_file, image_path, image_urls, image_frmt='.jpg'):
    '''Crawl JPG/GIF images with the given URLs.

    Parameters:
        txt_file <str> - The TXT file for saving information.
        image_path <str> - The path for saving images.
        image_urls <list> - The URLs of images.
        image_frmt <str> - The format of images. Default is '.jpg'.

    Return:
        0 <int> - If the task is completed.
    '''
    TIME_DELAY = 1

    # Set the tag of images (JPG or GIF).
    if image_frmt == '.jpg':
        del image_urls[0]  # The first JPG_URL (repeated) should not be used.
        tag_img = 'JPG'
    elif image_frmt == '.gif':
        tag_img = 'GIF'
    else:
        tag_img = 'unknown'

    # Crawl images.
    for i in range(len(image_urls)):
        # Save the URL of images to the TXT file.
        with open(txt_file, 'a', encoding='utf-8') as ff:
            ff.write('The link of the %d-th %s image is: %s\n' % (i + 1, tag_img, image_urls[i]))

        # Download images.
        path = image_path + str(i + 1) + image_frmt
        try:  # Try x1.
            print('Download the %d-th %s image.' % (i + 1, tag_img))
            urllib.request.urlretrieve(urllib.request.urlopen(image_urls[i]).geturl(), path)
            time.sleep(TIME_DELAY)
        except:  # Try again x2.
            try:
                print('Download the %d-th %s image.' % (i + 1, tag_img))
                urllib.request.urlretrieve(urllib.request.urlopen(image_urls[i]).geturl(), path)
                time.sleep(TIME_DELAY)
            except:  # Try again and again x3.
                try:
                    print('Download the %d-th %s image.' % (i + 1, tag_img))
                    urllib.request.urlretrieve(urllib.request.urlopen(image_urls[i]).geturl(), path)
                    time.sleep(TIME_DELAY)
                except:  # If failed.
                    print('*****Error: Failed to download the image:', image_urls[i])
                    with open(txt_file, 'a', encoding='utf-8') as ff:
                        ff.write('*****Error: Failed to download the image: %s\n' % image_urls[i])
                    time.sleep(TIME_DELAY)

    return 0


def crawl_photo(txt_file, photo_path, photo_urls, if_live2gif=False):
    '''Crawl live photos with the given URLs.

    Parameters:
        txt_file <str> - The TXT file for saving information.
        photo_path <str> - The path for saving live photos (videos).
        photo_urls <list> - The URLs of live photos (videos).
        if_live2gif <bool> - If convert live photos (videos) to GIF images. Default is False (not convert).

    Return:
        0 <int> - If the task is completed.
    '''
    TIME_DELAY = 1

    # Crawl live photos.
    for i in range(len(photo_urls)):
        # Save the URL of live photos to the TXT file.
        with open(txt_file, 'a', encoding='utf-8') as ff:
            ff.write('The link of the %d-th live photo is: %s\n' % (i + 1, photo_urls[i]))

        # Download live photos.
        path = photo_path + str(i + 1) + '.mov'
        try:  # Try x1.
            print('Download the %d-th live photo.' % (i + 1))
            urllib.request.urlretrieve(urllib.request.urlopen(photo_urls[i]).geturl(), path)
            time.sleep(TIME_DELAY)
        except:  # Try again x2.
            try:
                print('Download the %d-th live photo.' % (i + 1))
                urllib.request.urlretrieve(urllib.request.urlopen(photo_urls[i]).geturl(), path)
                time.sleep(TIME_DELAY)
            except:  # Try again and again x3.
                try:
                    print('Download the %d-th live photo.' % (i + 1))
                    urllib.request.urlretrieve(urllib.request.urlopen(photo_urls[i]).geturl(), path)
                    time.sleep(TIME_DELAY)
                except:  # If failed.
                    print('*****Error: Failed to download the live photo:', photo_urls[i])
                    with open(txt_file, 'a', encoding='utf-8') as ff:
                        ff.write('*****Error: Failed to download the live photo: %s\n' % photo_urls[i])
                    time.sleep(TIME_DELAY)

        # Convert live photos to GIF images.
        if os.path.isfile(path) and if_live2gif:
            video2gif(path, photo_path, str(i + 1) + '.gif')

    return 0


def crawl_video(txt_file, video_path, video_urls, video_frmt='.mp4'):
    '''Crawl videos with the given URLs.

    Parameters:
        txt_file <str> - The TXT file for saving information.
        video_path <str> - The path for saving videos.
        video_urls <str> - The URLs of videos.
        video_frmt <str> - The format of videos. Default is '.mp4'.

    Return:
        0 <int> - If the task is completed.
    '''
    TIME_DELAY = 1

    # Crawl videos.
    for i in range(len(video_urls)):
        # Save the information of videos to the TXT file.
        with open(txt_file, 'a', encoding='utf-8') as ff:
            ff.write('The link of the %d-th video is: null\n' % (i + 1))

        # Download videos.
        path = video_path + str(i + 1) + video_frmt
        try:  # Try x1.
            print('Download the %d-th video.' % (i + 1))
            urllib.request.urlretrieve(urllib.request.urlopen(video_urls[i]).geturl(), path)
            time.sleep(TIME_DELAY)
        except:  # Try again x2.
            try:
                print('Download the %d-th video.' % (i + 1))
                urllib.request.urlretrieve(urllib.request.urlopen(video_urls[i]).geturl(), path)
                time.sleep(TIME_DELAY)
            except:  # Try again and again x3.
                try:
                    print('Download the %d-th video.' % (i + 1))
                    urllib.request.urlretrieve(urllib.request.urlopen(video_urls[i]).geturl(), path)
                    time.sleep(TIME_DELAY)
                except:  # If failed.
                    print('*****Error: Failed to download the video:', video_urls[i])
                    with open(txt_file, 'a', encoding='utf-8') as ff:
                        ff.write('*****Error: Failed to download the video: %s\n' % video_urls[i])
                    time.sleep(TIME_DELAY)

    return 0
