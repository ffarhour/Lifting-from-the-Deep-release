#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 15 2018

@author: Farmehr Farhour'
"""
import os
import errno
import numpy as np

import cv2

def fio_print_to_file(in_filename, in_string):
    """ Writes a string to file """
    filename = in_filename + ".txt"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    #with open(in_filename, 'w') as f:
        #print >> f, in_string
    file = open(filename,"w")
    file.write(in_string)
    file.close()


def fio_save_pose_3d_text(in_filename, in_pose_3d):
    str1 = np.array2string(in_pose_3d)
    fio_print_to_file(in_filename, str1)

def fio_stitch_images_to_video(in_folder_name, video_name):
    "stitches all png files in the folder and saves as video_name"

    images = [img for img in os.listdir(in_folder_name) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(in_folder_name, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    video = cv2.VideoWriter(video_name, fourcc, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(in_folder_name, image)))

    cv2.destroyAllWindows()
    video.release()
