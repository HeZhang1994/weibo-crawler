'''Function (Python3): Python functions for Sina Weibo crawler.

Author: He Zhang @ University of Exeter
Date: April 17th 2019 (Update: April 17th 2019)
Contact: hz298@exeter.ac.uk

Copyright (c) 2019 He Zhang
'''

import os
import re
import shutil
from subprocess import check_output

import cv2
import imageio
from PIL import Image


def time_str2float(time_str):
    '''Convert time from string to floating number.

    Parameter:
        time_str <class 'str'> - The string of time formatted as 'hh:mm:ss.nnn'.

    Return:
        time_flt <class 'float'> - The floating number of time formatted as 'ss.nnn'.
    '''
    time_list = re.split('[:]', time_str)
    time_flt = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + float(time_list[2])

    return time_flt


def get_video_duration(video_path):
    '''Get the duration of a video.

    Parameter:
        video_path <class 'str'> - The path of input video.

    Return:
        video_duration <class 'str'> - The duration of video formatted as 'hh:mm:ss.nnn'.
    '''
    # Create the command for getting the information of video via ffprobe.
    cmd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', video_path]
    # Get the information of video via ffprobe command.
    out_byte = check_output(cmd)  # <class 'bytes'>
    # Decode the information of video from 'bytes' to 'str'.
    out_str = out_byte.decode("utf-8")  # <class 'str'>
    # Split the information of video from 'str' to 'list'.
    out_list = re.split('[\n]', out_str)  # <class 'list'>

    # Get the duration of video.
    for info in out_list:
        if 'duration' in info:
            # E.g., 'info' = 'duration=0:00:01.860000'
            video_duration = re.split('[=]', info)[1]  # <class 'str'>

    return video_duration


def image_resizer(image_path, ratio=0.4):
    '''Resize an image.

    Parameters:
        image_path <class 'str'> - The path of input image.
        ratio <class 'float'> - The ratio for resizing image. Default is '0.4'.

    Return:
        0 <class 'int'> - If image resizing is completed.
    '''
    img = Image.open(image_path)
    width, height = img.size
    img = img.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
    img.save(image_path)

    return 0


def gif_creator(gif_path, gif_duration, frame_folder, frame_format='.jpg'):
    '''Create a GIF image with the given video frames.

    Parameters:
        gif_path <class 'str'> - The path of output GIF image.
        gif_duration <class 'float'> - The total duration of output GIF image.
        frame_folder <class 'str'> - The folder of input video frames.
        frame_format <class 'str'> - The format of input video frames. Default is '.jpg'.

    Return:
        0 <class 'int'> - If GIF creation is completed.
    '''
    imgGIF = []

    # Get the sorted name of frames.
    imgFames = sorted((iN for iN in os.listdir(frame_folder) if iN.endswith(frame_format)))

    # Calculate the duration of each frame.
    frame_duration = gif_duration / len(imgFames)

    # Create the GIF image with frames.
    for imgFame in imgFames:
        # Resize each frame to reduce the size of GIF image.
        image_resizer(frame_folder + imgFame)
        # Concatenate each frame.
        imgGIF.append(imageio.imread(frame_folder + imgFame))

    # Save GIF image.
    imageio.mimsave(gif_path, imgGIF, duration=frame_duration)

    return 0


def video2gif(video_path, gif_folder, gif_name):
    '''Convert a video to a GIF image.

    Parameters:
        video_path <class 'str'> - The path of input video.
        gif_folder <class 'str'> - The folder for saving output GIF image.
        gif_name <class 'str'> - The name of output GIF image.

    Return:
        0 <class 'int'> - If conversion is completed.
    '''
    # Initialize a temporary folder for saving video frames.
    folder_tmp = gif_folder + 'tmp/'
    if os.path.exists(folder_tmp):
        shutil.rmtree(folder_tmp)
    os.mkdir(folder_tmp)

    # Extract and save video frames to the temporary folder.
    vidcap = cv2.VideoCapture(video_path)  # <class 'cv2.VideoCapture'>
    success, image = vidcap.read()  # 'success' <class 'bool'>, 'image' <class 'numpy.ndarray'>
    count = 0
    while success:
        path = folder_tmp + 'frame_' + str(count).zfill(3) + '.jpg'
        cv2.imwrite(path, image)  # Save each frame as an image.
        success, image = vidcap.read()
        count += 1

    # Get the duration of video (seconds).
    duration_str = get_video_duration(video_path)
    duration_flt = time_str2float(duration_str)

    # Create the GIF image of video.
    gif_creator(gif_folder + gif_name, duration_flt, folder_tmp)

    # Delete the temporary folder.
    if os.path.exists(folder_tmp):
        shutil.rmtree(folder_tmp)

    return 0
