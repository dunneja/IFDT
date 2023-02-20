#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : cfg_func.py
# Application  : Intelligent File Delivery Tool.
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : MIT-license
# Comment      : This file is part of IFDT.
# ----------------------------------------------------------------------------
# Import python core modules.
import os.path
from configparser import ConfigParser

class config_file():
    """
    A Class to represent a config file
    """
    def __init__(self, config_file):
        """
        Initialisation
        Define a config file variable.
        """
        self.config_file = config_file
        self.check_conf()

    def check_conf(self):
        """
        Create a conf file if one does not exist
        """
        # Check if the config_file exists.
        if (os.path.isfile(self.config_file)):
            print(f' * config File {self.config_file} exists!')
        # If the config_file does not exist then create a template.
        elif (os.path.isfile(self.config_file)) == False:
            print(f' * config file {self.config_file} does not exist!')
            # Create a config layout.
            config = ConfigParser()
            # Read the config file
            config.read(self.config_file)
            config.add_section('main')
            config.set('main', 'log_dir', 'logs')
            config.set('main', 'output_dir', 'output')
            config.add_section('file_input')
            config.set('file_input', 'doctype1_dir', 'input\doctype1')
            config.set('file_input', 'doctype2_dir', 'input\doctype2')
            config.set('file_input', 'doctype3_dir', 'input\doctype3')
            config.add_section('file_output')
            config.set('file_output', 'doctype1_ext', 'MJC_')
            config.set('file_output', 'doctype2_ext', 'UNK_')
            config.set('file_output', 'doctype3_ext', 'SI_')
            config.add_section('ocr')
            config.set('ocr', 'strip_values', '/.')
            config.set('ocr', 'file_format', '.pdf')
            config.set('ocr', 'doctype1_zone', '26')
            config.set('ocr', 'doctype2_zone', '20')
            config.set('ocr', 'doctype3_zone', '133')
            # Write the config layout to an ini file.
            with open(str(self.config_file), 'w') as f:
                config.write(f)
                print(f' * creating config file {self.config_file}.')
