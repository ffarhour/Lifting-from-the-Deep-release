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
from os.path import dirname, realpath

import argparse

import helpers

DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
IMAGE_FILE_PATH = PROJECT_PATH + '/data/images/test_image.png'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'


def main(args):

    # argparse
    parser = argparse.ArgumentParser(description='Lifting from the Deep')
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--outputtype', '-t', nargs='+', type=str, metavar='<type of output>', choices=["disp","text","images","video"], help='types of output, e.g. display only, images, text, video. If not provided, no output will be written to file.', required=True)
    requiredNamed.add_argument('--output', '-o', type=str, metavar='<output folder name>', help='the folder name to store the output', required=True)
    optionalArgs = parser.add_argument_group('Optional Arguments')


    args = parser.parse_args()
    print(args)


    image = cv2.imread(IMAGE_FILE_PATH)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb

    # create pose estimator
    image_size = image.shape

    pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

    # load model
    pose_estimator.initialise()

    # estimation
    pose_2d, visibility, pose_3d = pose_estimator.estimate(image)

    # close model
    pose_estimator.close()

    handle_output(image, pose_2d, visibility, pose_3d, args.output, args.outputtype)

    # Show 2D and 3D poses
    #draw_results(image, pose_2d, visibility, pose_3d)


def draw_results(in_image, data_2d, joint_visibility, data_3d, do_save_as_image=False, do_display=False, filename=""):
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
        my_plot.savefig(filename + str(index) + ".png")
        index+=1

    if(do_display):
        plt.show()


def handle_output(in_image, data_2d, joint_visibility, data_3d, in_output_name, in_output_type):
    # process output name
    filename = in_output_name + "/" + "0"

    if("text" in in_output_type):
        helpers.fio_save_pose_3d_text(filename, data_3d)

    # set variables to know what to do
    do_save_as_image = False
    do_save_as_video = False
    do_display_images = False
    if("images" in in_output_type):
        do_save_as_image = True
    if("video" in in_output_type):
        do_save_as_video = True
    if("disp" in in_output_type):
        do_display_images = False

    draw_results(in_image, data_2d, joint_visibility, data_3d, do_save_as_image, do_display_images, filename)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
