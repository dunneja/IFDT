#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : dir_func.py
# Application  : Intelligent File Delivery Tool.
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : MIT-license
# Comment      : This file is part of IFDT.
# ----------------------------------------------------------------------------
""" Check directory functions. """
# Import modules.
from functions import log_func as log_func
import os

def chk_log_dir(log_dir):
    """
    check if the log dir exists if not make.
    """
    if (os.path.isdir(log_dir)):
        print(f' * {log_dir} directory exists!')
    else:
        try:
            print(f" * {log_dir} directory doesn't exist!")
            os.mkdir(log_dir)
            print(f' * Sucessfully created the {log_dir} directory.')
            emsg = f'Sucessfully created the {log_dir} directory.'
            log_func.logw('sys_log', emsg)
        except OSError:
            print(f' * Creation of the {log_dir} directory failed.')

def chk_input_dir(input_dir):
    """
    check if the input dir exists if not make.
    """
    if (os.path.isdir(input_dir)):
        print(f' * {input_dir} directory exists!')
    else:
        try:
            print(f" * {input_dir} directory doesn't exist!")
            os.mkdir(input_dir)
            print(f' * Sucessfully created the {input_dir} directory.')
            emsg = f'Sucessfully created the {input_dir} directory.'
            log_func.logw('sys_log', emsg)
        except OSError:
            print(f' * Creation of the {input_dir} directory failed.')
            emsg = f' * Creation of the {input_dir} directory failed.'
            log_func.logw('sys_log', emsg)

def chk_output_dir(output_dir):
    """
    check if the output dir exists if not make.
    """
    if (os.path.isdir(output_dir)):
        print(f' * {output_dir} directory exists!')
    else:
        try:
            print(f" * {output_dir} directory doesn't exist!")
            os.mkdir(output_dir)
            print(f' * Sucessfully created the {output_dir} directory.')
            emsg = f'Sucessfully created the {output_dir} directory.'
            log_func.logw('sys_log', emsg)
        except OSError:
            print(f' * Creation of the {output_dir} directory failed.')
            emsg = f' * Creation of the {output_dir} directory failed.'
            log_func.logw('sys_log', emsg)