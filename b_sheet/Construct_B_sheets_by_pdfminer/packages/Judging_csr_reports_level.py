import os
import pdfminer
import fitz
import pandas as pd
import sys
import re
import pdfplumber
import pylint
import traceback
from PIL import Image
import numpy as np
import argparse
from Exception_handling import get_exception

class judging_csr_reports_level:
    
    def __init__(self, csr_report_path):
        self.csr_report_path = csr_report_path
        self._files_list = os.listdir(self.csr_report_path)
        self._corporate_name = []
        self._picture_amount = []
        self._level = []
        
    
    def judge_csr_reports_difficulty(self):
        """
        judge_csr_reports_difficulty [summary]
            Define each difficuty of dealing with the contents of csr report.
            
            When the total amounts of picutures in report is greater than 10, 
            the set it to level 2,which means the report itself is difficulte to parse.
            
            In other words, the level 1s should be the top priority to parse.
        """
        try:
            for file in self.get_files_list():

                print(f'Now processing {file}, judging levels ')

                picture_amt = 0
                current_file = os.path.join(self.csr_report_path, file)
                pdf_document = fitz.open(current_file)
                pdf_plumber_document = pdfplumber.open(current_file)

                for current_page in range(len(pdf_document)):
                    # The count of picture amounts will assigned to picture_amt
                    picture_amt = self.__count_picture_amts_in_current_page(
                        pdf_plumber_document,
                        pdf_document,
                        current_page,
                        picture_amt=picture_amt)

                self.get_corporate_name().append(file)
                self.get_picture_amount().append(picture_amt)
                self.get_level().append(
                    self.__judge_current_report_level(picture_amt))

            #Output level csv file
            dict = {
                "Corporate Name": self.get_corporate_name(),
                "Picture Amounts": self.get_picture_amount(),
                "Level": self.get_level(),
            }
            self.__output_csv(dict=dict,
                              index='Corporate Name',
                              sort_value='Level',
                              csv_name='process_list')
            print(f'Judging Completed : output file')
        except Exception as e:
            get_exception(e, file)

    def __judge_current_report_level(self, picture_amt: int) -> int:
        """
        judge_current_report_level [summary]
            Judge the difficuty level of current report.
            If picture amounts is greater than 10, then set level 2,otherwise,1 
        Args:
            picture_amt (int): [description] the total pictures amounts of current report
        Returns:
            int: [description] the difficuty level of current csr report
        """
        if picture_amt > 10:
            lvl = 2
        else:
            lvl = 1
        return lvl

    def __output_csv(self, dict: dict, index: str, sort_value: str,
                     csv_name: str):
        """
        output_csv [summary]
            output the GRI pointers of B sheet as csv file 
        Args:
            dict (dict): [description] the dictionary which used to create a dataframe.
            index (str): [description] the specified column used to be as index.
            sort_value (str): [description] the specified column used to sort.
            csv_name (str): [description] the output file name
        """
        df = pd.DataFrame(dict)
        df = df.sort_values(sort_value, ascending=True)
        df = df.set_index(index)
        df.to_csv(f'{csv_name}.csv', encoding="utf_8_sig")

    def __count_picture_amts_in_current_page(self, pdf_plumber_document,
                                             pdf_document, current_page,
                                             picture_amt):
        """
        count_picture_amts_in_current_page [summary]
            parse current page of certain csr report, 
            and count the number of pictures in the csr report 
        Args:
            pdf_plumber_document ([type]pdf_plumber.open(file)): [description]
                the csr report open with pdf_plumber to get the current page.
                
            pdf_document ([type] fitz.open(file)): [description] 
                the csr report open with fitz to get image in current page.
            
            current_page ([type] number): [description] 
                the number of parsing current page
        """
        page = pdf_plumber_document.pages[current_page]
        for image in pdf_document.getPageImageList(current_page):
            xref = image[0]
            pix = fitz.Pixmap(pdf_document, xref)
            if pix.n < 5:  # this is GRAY or RGB
                if int(pix.height) >= int(page.height) and int(
                        pix.width) >= int(page.width):
                    picture_amt = picture_amt + 1
                    pix = None
                else:  # CMYK: convert to RGB first
                    if int(pix.height) >= int(page.height) and int(
                            pix.width) >= int(page.width):
                        picture_amt = picture_amt + 1
                        pix = None
        return picture_amt

    def set_csr_report_path(self, new_csr_report_path: str):
        self.csr_report_path = new_csr_report_path

    def set_corporate_name(self, corporate_name: str):
        self._corporate_name = corporate_name

    def set_picture_amount(self, new_picture_amount: int):
        self._picture_amount = new_picture_amount

    def set_level(self, new_level):
        self._level = new_level

    def get_corporate_name(self):
        return self._corporate_name

    def get_picture_amount(self):
        return self._picture_amount

    def get_level(self):
        return self._level

    def get_files_list(self):
        return self._files_list

    def get_csr_report_path(self):
        return self.csr_report_path