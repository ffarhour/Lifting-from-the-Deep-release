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

def fio_stitch_images_to_video(in_folder_name, start_frame):
    "stitches all png files in the folder and saves as video_name"

    images = [img for img in os.listdir(in_folder_name) if img.endswith(".png")]

    # find number of people in the image
    number_of_people = 0
    images_frame_names = []
    person_id_list = []
    for image in images:
        person_id = int(image.split("_")[0])
        if person_id not in person_id_list:
            number_of_people += 1
            person_id_list.append(person_id)

        # get all images without person id
        images_frame_names += image.split("_")[1:]

    number_of_frames = len(set(images_frame_names))
    print(number_of_frames)

    for i in person_id_list: # for every person
        image_filename = str(i) + "_" + str(start_frame) + ".png"
        frame = cv2.imread(os.path.join(in_folder_name, image_filename))
        height, width, layers = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        video_name = in_folder_name + str(i) + ".avi"
        video = cv2.VideoWriter(video_name, fourcc, 30, (width,height))
        for frames in range(0, number_of_frames): # for every frame
            image_filename = str(i) + "_" + str(frames + start_frame) + ".png"
            print("getting " + image_filename)
            frame = cv2.imread(os.path.join(in_folder_name, image_filename))
            frame = cv2.resize(frame, (width,height))
            video.write(frame)
        video.release()
        cv2.destroyAllWindows()
