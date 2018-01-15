#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 15 2018

@author: Farmehr Farhour'
"""
import os
import errno
import numpy as np


def fio_print_to_file(in_filename, in_string):
    """ Writes a string to file """
    if not os.path.exists(os.path.dirname(in_filename)):
        try:
            os.makedirs(os.path.dirname(in_filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    #with open(in_filename, 'w') as f:
        #print >> f, in_string
    file = open(in_filename,"w") 
    file.write(in_string)
    file.close()
    
    
def fio_save_pose_3d_text(in_filename, in_pose_3d):
    str1 = np.array2string(in_pose_3d)
    fio_print_to_file(in_filename, str1)


