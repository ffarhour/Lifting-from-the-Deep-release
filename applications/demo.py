#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Dec 20 17:39 2016

@author: Denis Tome
@author: Farmehr Farhour
"""

import __init__

from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose

import cv2
import matplotlib.pyplot as plt
from os.path import dirname, realpath, splitext
import os

import argparse

import helpers

DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
#IMAGE_FILE_PATH = PROJECT_PATH + '/data/images/test_image.png'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'

def CheckExt(choices):
    class Act(argparse.Action):
        def __call__(self,parser,namespace,fname,option_string=None):
            ext = os.path.splitext(fname)[1][1:]
            if ext not in choices:
                option_string = '({})'.format(option_string) if option_string else ''
                parser.error("file doesn't end with one of {}{}".format(choices,option_string))
            else:
                setattr(namespace,self.dest,fname)

    return Act

def main(args):
    # argparse
    parser = argparse.ArgumentParser(description='Lifting from the Deep')
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--outputtype', '-t', nargs='+', type=str, metavar='<type of output>', choices=["disp","text","images","video"], help='types of output, e.g. display only, images, text, video. If not provided, no output will be written to file.', required=True)
    requiredNamed.add_argument('--output', '-o', type=str, metavar='<output folder name>', help='the folder name to store the output', required=True)
    requiredNamed.add_argument('--input', '-i', action=CheckExt({'mp4','avi','png'}), metavar='<input file name>', help='the filename input. acceptable formats', required=True)
    optionalArgs = parser.add_argument_group('Optional Arguments')
    optionalArgs.add_argument('--startframe', '-s', type=int, metavar='<start frame number of input>', help='the start frame number of the input video', required=False)
    optionalArgs.add_argument('--endframe', '-e', type=int, metavar='<end frame number of input>', help='the end frame number of the input video', required=False)
    args = parser.parse_args()

    # process output name
    args.output = args.output + "/"

    # check if video or image
    if(args.input.endswith('.mp4') or args.input.endswith('.avi')):
        cap = cv2.VideoCapture(args.input)
        # get frames and process frame by frame
        frame_index = 0
        if cap.isOpened() and args.startframe is not None:
            for i in range(0, args.startframe):
                cap.read()
                frame_index += 1
        while(cap.isOpened()):
            if args.endframe is not None:
                if(frame_index>args.endframe):
                    break
            ret, frame = cap.read()
            cv2.imwrite(args.output + "9_%d.png" % frame_index, frame) # write the input video as images as well
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #image = cv2.imread(args.output + "%d.png" % frame_index)
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb
            process_image(image, args.output, args.outputtype, frame_index)
            frame_index += 1

        cap.release()
        cv2.destroyAllWindows()
        handle_video_output(args.output, args.outputtype, args.startframe)

    else: # an image
        image = cv2.imread(args.input)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb
        process_image(image, args.output, args.outputtype)


def process_image(image, output, outputtype, video_frame_num=0):
    # create pose estimator
    image_size = image.shape
    pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

    # load model
    pose_estimator.initialise()

    # estimation
    pose_2d, visibility, pose_3d = pose_estimator.estimate(image)

    # close model
    pose_estimator.close()

    handle_frame_output(image, pose_2d, visibility, pose_3d, output, outputtype, video_frame_num)


def draw_results(in_image, data_2d, joint_visibility, data_3d, do_save_as_image=False, do_display=False, filename="", video_frame_num=0):
    """Plot 2D and 3D poses for each of the people in the image."""
    plt.figure()
    draw_limbs(in_image, data_2d, joint_visibility)
    plt.imshow(in_image)
    plt.axis('off')

    # Show 3D poses
    index = 0
    for single_3D in data_3d:
        # or plot_pose(Prob3dPose.centre_all(single_3D))
        my_plot = plot_pose(single_3D)
        my_plot.savefig(filename + str(index) + "_" + str(video_frame_num) + ".png")
        index+=1

    if(do_display):
        plt.show()

    plt.close()

def handle_video_output(output_name, output_type, start_frame=0):
    if("video" in output_type):
        helpers.fio_stitch_images_to_video(output_name,start_frame)

def handle_frame_output(in_image, data_2d, joint_visibility, data_3d, output_name, output_type, video_frame_num=0):
    if("text" in output_type):
        helpers.fio_save_pose_3d_text(output_name, data_3d)

    # set variables to know what to do
    do_save_as_image = False
    do_save_as_video = False
    do_display_images = False
    if("images" in output_type):
        do_save_as_image = True
    if("disp" in output_type):
        do_display_images = True

    draw_results(in_image, data_2d, joint_visibility, data_3d, do_save_as_image, do_display_images, output_name, video_frame_num)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
