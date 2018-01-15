#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Dec 20 17:39 2016

@author: Denis Tome'
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
    optionalArgs = parser.add_argument_group('Optional Arguments')
    requiredNamed.add_argument('--outputtype', '-t', type=str, metavar='<type of output>', choices=["text","images","video"], help='types of output, e.g. images, text, video. If not provided, no output will be written to file.', required=True)
    requiredNamed.add_argument('--output', '-o', type=str, metavar='<output file name>', help='the file name', required=True)

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
    
    write_pose_3d(pose_3d, args.output, args.outputtype)

    # Show 2D and 3D poses
    display_results(image, pose_2d, visibility, pose_3d)
    

def display_results(in_image, data_2d, joint_visibility, data_3d):
    """Plot 2D and 3D poses for each of the people in the image."""
    plt.figure()
    draw_limbs(in_image, data_2d, joint_visibility)
    plt.imshow(in_image)
    plt.axis('off')

    # Show 3D poses
    for single_3D in data_3d:
        # or plot_pose(Prob3dPose.centre_all(single_3D))
        plot_pose(single_3D)

    plt.show()
    

def write_pose_3d(in_pose_3d, in_output_name, in_output_type):
    # create an array of output type to match
    output_type_array = in_output_type.split()
    
    if(output_type_array[0] == "text"):
        helpers.fio_save_pose_3d_text(in_output_name, in_pose_3d)
    elif(output_type_array[0] == "images"):
        print("nothing")
    elif(output_type_array[0] == "video"):
        print("nothing")
    


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
