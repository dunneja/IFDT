#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : ifdt.py
# Application  : Intelligent File Delivery Tool.
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : MIT-license
# Comment      : This file is part of IFDT.
# ----------------------------------------------------------------------------
"""
Intelligent File Delivery Tool.
"""
import os
import cv2
from pytesseract import Output, pytesseract
from functions import cfg_func, dir_func, log_func
from configparser import ConfigParser

def interface():
    """
    Function to define a basic console interface
    """
    try:
        while True:   
            line = '-' * 50
            print('\n' + line)
            print('Intelligent File Delivery Tool - Interface Menu')
            print(line)
            print('\n Ensure Each Document Type Is Located In Each')
            print(' Input Folder Type Before Selecting Options.\n')
            print(line)
            print('\n1) Process Document - Type 1')
            print('2) Process Document - Type 2')
            print('3) Process Document - Type 3')
            print('4) Select OCR Zone  - Type 4\n')
            print(line)
            selection = input("\nSelect Document Type [1-4] or 'CTRL-C' to Quit: ")
            if selection == '1':
                OcrProcess(1)
            elif selection == '2':
                OcrProcess(2)
            elif selection == '3':
                OcrProcess(3)
            elif selection == '4':
                ocr_zone_value()
            else:
                print('\nInvalid Selection, Please Select [1-3]\n')   
    except KeyboardInterrupt:
        cls = lambda: os.system('cls')
        cls()
        pass

class OcrProcess():
    """
    A class to process ocr a file and extract text.
    Based on extracted value a pdf will be created
    with the extracted value as it's name.
    """
    def __init__(self, doc_type):
        """
        Class initialisation.
        Define global variables.
        """
        self.doc_type = doc_type
        self.main()
        
    def main(self):
        """
        Main function to call all other functions!
        """
        self.header()
        self.config_files()
        self.doc_type_select()

    def header(self):
        """
        Console Interface Header Function
        """
        line = '-' * 50
        print('\n' + line)
        print(f'IFDT - Document Type {self.doc_type} Processing..')
        print(line)

    def config_files(self):
        """
        Function to define and process config information.
        this function will call chk_output and chk_log.
        """
        config_file = 'ifdt.conf'
        cfg_func.config_file(config_file)
        # Read the config_file contents.
        config = ConfigParser()
        config.read(config_file)
        self.output_dir = config.get('main', 'output_dir')
        self.log_dir = config.get('main', 'log_dir')
        self.doctype1_dir = config.get('file_input', 'doctype1_dir')
        self.doctype2_dir = config.get('file_input', 'doctype2_dir')
        self.doctype3_dir = config.get('file_input', 'doctype3_dir')
        self.doctype1_ext = config.get('file_output', 'doctype1_ext')
        self.doctype2_ext = config.get('file_output', 'doctype2_ext')
        self.doctype3_ext = config.get('file_output', 'doctype3_ext')
        self.doctype1_zone = config.get('ocr', 'doctype1_zone')
        self.doctype2_zone = config.get('ocr', 'doctype2_zone')
        self.doctype3_zone = config.get('ocr', 'doctype3_zone')
        self.docname_strip = config.get('ocr', 'strip_values')
        self.doc_file_format = config.get('ocr', 'file_format')
        dir_func.chk_log_dir(self.log_dir)
        dir_func.chk_input_dir(self.doctype1_dir)
        dir_func.chk_input_dir(self.doctype2_dir)
        dir_func.chk_input_dir(self.doctype3_dir)
        dir_func.chk_output_dir(self.output_dir)

    def doc_type_select(self):
        """
        Document type selection function.
        Doc type will be specified and read_dir called.
        """
        if self.doc_type == 1:
            doctype1_dir = self.doctype1_dir
            self.read_dir(doctype1_dir, doc_value=1)
        elif self.doc_type == 2:
            doctype2_dir = self.doctype2_dir
            self.read_dir(doctype2_dir, doc_value=2)
        elif self.doc_type == 3:
            doctype3_dir = self.doctype3_dir
            self.read_dir(doctype3_dir, doc_value=3)
        else:
            print(' * Unknown Doc Type Selected!')

    def read_dir(self, dir, doc_value):
        """
        Function to read all the filenames in a dir.
        Each file will be processed and passed to,
        tiff_ocr_extract function.
        """
        count = 1
        for subdir, dirs, files in os.walk(dir):
            for file in files:
                file_name = os.path.join(subdir, file)
                print(f' * Processing {count} of {len(files)} files.')
                self.tiff_ocr_extract(file_name, doc_value)
                count +=1

    def tiff_ocr_extract(self, file_name, doc_value):
        """
        Take a tiff file, ocr it and extract text.
        Extract value and assign to a variable.
        Extracted variable will then be sent to 
        tiff_to_pdf function.
        """
        # Read image to extract text from image
        img = cv2.imread(file_name)
        # Convert image to grey scale
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Converting grey image to binary image by Thresholding.
        # This results in better OCR.
        thresh_img = cv2.threshold(
            gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # configuring parameters for tesseract
        custom_config = r'--oem 3 --psm 6'
        # Comment this out for Linux Systems.
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # Get all OCR output information from pytesseract
        ocr_output_details = pytesseract.image_to_data(
            thresh_img, output_type=Output.DICT, config=custom_config, lang='eng')
        # Print OCR Output keys.
        # print(ocr_output_details.keys())
        for k, v in ocr_output_details.items():
            if k == 'text':
                if doc_value == 1:
                    doc_ext = self.doctype1_ext
                    #doc_type_value1 = self.doctype1_zone
                    self.extracted_value = v[int(self.doctype1_zone)]
                    msg = (f' * Extracted Value: {self.extracted_value} from {file_name}')
                    print(msg)
                    log_func.logw('processing', msg)
                    #self.tiff_to_pdf(doc_ext, file_name)
                    self.searchable_pdf(file_name)
                elif doc_value == 2:
                    doc_ext = self.doctype2_ext
                    #doc_type_value2 = self.doctype2_zone
                    self.extracted_value = v[int(self.doctype2_zone)]
                    msg = (f' * Extracted Value: {self.extracted_value} from {file_name}')
                    print(msg)
                    log_func.logw('processing', msg)
                    #self.tiff_to_pdf(doc_ext, file_name)
                    self.searchable_pdf(file_name)
                elif doc_value == 3:
                    doc_ext = self.doctype3_ext
                    #doc_type_value3 = self.doctype3_zone
                    self.extracted_value = v[int(self.doctype3_zone)]
                    msg = (f' * Extracted Value: {self.extracted_value} from {file_name}')
                    print(msg)
                    log_func.logw('processing', msg)
                    #self.tiff_to_pdf(doc_ext, file_name)
                    self.searchable_pdf(file_name)
                else:
                    print()
                    msg = (f' * Unknown doc type for {file_name}')
                    print(msg)
                    log_func.logw('processing', msg)

    def searchable_pdf(self, tiff_path: str) -> str:
        """
        Function to create a searchable PDF.
        """
        # Striped specified values from filename value.
        new_pdf_filename = self.extracted_value.strip(self.docname_strip)
        # Strip any forward slashes from the string value.
        new_pdf_filename = new_pdf_filename.replace("/", "")
        # Define the new pdf file name using extracted value.
        pdf_filename = new_pdf_filename + self.doc_file_format
        if not os.path.exists(tiff_path):
            raise Exception(f'{tiff_path} does not exist.')
        # Comment this out for Linux Systems.
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        PDF = pytesseract.image_to_pdf_or_hocr(tiff_path, extension='pdf')
        msg = (f' * Converting {tiff_path} to {self.output_dir}\{pdf_filename}')
        print(msg)
        log_func.logw('processing', msg)
        # Export to searchable pdf
        with open(self.output_dir + '/' + pdf_filename, 'w+b') as f:
            f.write(bytearray(PDF))
        msg = (f' * Created Searchable PDF in {self.output_dir}\{pdf_filename}')
        print(msg)
        log_func.logw('processing', msg)

def ocr_zone_value():
    """
    Take a tiff file, ocr it and extract text.
    extract WO value and assign to a variable.
    """
    # Obtain file name from user.
    file_name = input('\nEnter File Name: ')
    # Obtain document value to be identified.
    ext_value = (input('Enter Value To Be Found: '))
    # Read image to extract text from image
    img = cv2.imread(file_name)
    # Convert image to grey scale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Converting grey image to binary image by Thresholding.
    # This results in better OCR.
    thresh_img = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # configuring parameters for tesseract
    custom_config = r'--oem 3 --psm 6'
    # Comment this out for Linux Systems.
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # Get all OCR output information from pytesseract
    ocr_output_details = pytesseract.image_to_data(
        thresh_img, output_type=Output.DICT, config=custom_config, lang='eng')
    # Print OCR Output keys.
    # print(ocr_output_details.keys())
    # print(ocr_output_details.values())
    d = ocr_output_details
    try:
        for k, v in d.items():
            if k == 'text':
                output = v.index(ext_value)
                print(f'Detected Value! OCR Dict Postion / Zone Value: {output}')
    except ValueError as ve:
        print(
            f'\nYou entered {ext_value} which was not in the OCR Dictionary.\n')

if __name__ == "__main__":
    interface()