import os
import fitz
import pandas as pd
import re
import numpy as np
from packages.Exception_handling import get_exception
import datetime
from packages.pointers_transfer import transfer_numbers



class GRIPointers_B:
    def __init__(self, csr_report_path: str, gri_pointers_csv_name: str):
        self.csr_report_path = csr_report_path
        self._files_list = os.listdir(self.csr_report_path)
        self.gri_pointers_csv_name = gri_pointers_csv_name
        self.csv_file = ''
        self.current_gri_pointer_number = 0
        self.reveal_number = 0
        self.pattern = ''

    #每間公司
    def catch_gri_pointers(self, csr_report_path: str, search_term: str):
        """
        catch_gri_pointers [summary]
            Detect gri pointers in each page including search_term 
        Args:
            csr_report_path (str): [description]  csr reports path
            search_term(str): search for the specified word in each page in each csr report file like "GRI 準則揭露項目"
        Returns:
            [type]: [description] completed csv file with b sheets
        """

        #init the requirment for the method
        current_company_number = 0  # to avoid the index in the first row

        try:
            for file in self.get_files_list():

                print(f'Now processing {file}')

                self.__fill_into_GRI_csv(
                    file=file,
                    pdf_document=fitz.open(os.path.join(csr_report_path,
                                                        file)),
                    current_company_number=current_company_number,
                    search_term=search_term)

                current_company_number = self.__shift_to_next_company(
                    current_company_number=current_company_number)

        except Exception as e:
            get_exception(e, file)

    #每間公司報告的每頁
    def __fill_into_GRI_csv(self, pdf_document, file, current_company_number,
                            search_term):
        """
        __fill_into_GRI_csv [summary] First initialize all the corporate name into
        csv files, then check each GRI pointers for each corporate. If ends, then do nothing.
        Args:
            pdf_document ([type]): [description]
            file ([type]): [description]
            current_company_number ([type]): [description]
            search_term ([type]): [description]
        """

        # First inserting all the corporates name into csv file.
        self.__fill_corporate_name(
            file=file, current_company_number=current_company_number)
        self.__shift_to_next_gri_pointer()
        #從這裡開始，所有的gri_pointer都從1開始

        #邏輯為，每一頁抓到Search term後，利用Regular expression存入list，一一比照dataframe的column與list內部項目
        #若list無比對成功者，該指標填0，換到下一個指標。
        #若list比對成功者，該指標填1
        ##########################################
        # Crawl into each page of current csr, if catch gri keywords then insert it into csv files
        for current_page in range(len(pdf_document)):
            self.__reset_gri_pointer()
            # Every page should traversal all the gri pointer
            page = pdf_document.loadPage(current_page)

            # 抓到每篇CSR報告附錄的GRI指標對照表
            if page.searchFor('GRI') or page.searchFor(
                        "指標") or page.searchFor("揭露") or page.searchFor("附錄"):
                print(page)
                self.__fill_into_single_csv(current_company_number, page)

        #抓到已揭露指標的數目
        for temp in range(1, 142):
            if self.csv_file.iat[current_company_number, temp] == 1:
                self.reveal_number += 1
            else:
                continue

        #每間公司結束之後，將該公司的揭露指標數與未揭露指標數填入dataframe
        self.__fill_in_each_reports_reveal_and_unreveal_numbers(
            current_company_number)
        self.reveal_number = 0

    #每間公司報告內部抓到的每頁揭露指標與column進行比對
    def __fill_into_single_csv(self, current_company_number, page):
        #Using normal expression to filter words caught.
        gri_pointers_disclosed_in_this_page = self.__gri_text_filter(
            re.findall(self.pattern, page.getText("text")))
        gri_pointers_disclosed_in_this_page = transfer_numbers(gri_pointers_disclosed_in_this_page)
        print(gri_pointers_disclosed_in_this_page)
        ##########################################
        for column in self.csv_file.columns:
            ####################################
            #處理是否揭露的判斷式
            if (column in gri_pointers_disclosed_in_this_page):
                self.csv_file.at[current_company_number, column] = 1
                
        for column in self.csv_file.columns:
            ####################################
            #處理是否揭露的判斷式
            if self.csv_file.at[current_company_number, column] == '':
                self.csv_file.at[current_company_number, column] = 0

    ################################################################
    #basic functions

    def init_gri_pointers_csv_file(self, csv_name):
        """
        init_gri_pointers_csv_file [summary] Initailizing the gri pointers csv file with following task:
        1. remove unnamed column
        2. remove all nan column being regarded as float type, u
        nabling to process with str type

        Args:
            csv_name ([type]): [description] the unprocessed initial csv name 

        Returns:
            [type]: [description] the processed csv file
        """

        self.csv_file = pd.read_csv(f'{csv_name}.csv')
        self.csv_file = self.csv_file.loc[:, ~self.csv_file.columns.str.
                                          contains('^Unnamed')]
        self.csv_file = self.csv_file.replace(np.nan, '',
                                              regex=True)  # All data frame
        return self.csv_file

    def __is_contain_hyphen(self, text) -> bool:
        is_hyphen = False
        for single_char in text:
            if single_char == "-":
                is_hyphen = True
        return not is_hyphen

    def __fill_in_each_reports_reveal_and_unreveal_numbers(
            self, current_company_number):
        self.csv_file.iat[current_company_number, -2] = self.reveal_number
        self.csv_file.iat[current_company_number,
                          -1] = 136 - self.reveal_number

    def __fill_corporate_name(self, file, current_company_number):
        self.csv_file.iat[current_company_number, 0] = file

    def __shift_to_next_gri_pointer(self):
        self.current_gri_pointer_number += 1

    def __reset_gri_pointer(self):
        self.current_gri_pointer_number = 1

    def __shift_to_next_company(self, current_company_number: int) -> int:
        """
        __shift_to_next_company [summary] shift to process next company's gri pointers
        
        Args:
            current_company_number ([type]): [description] 
        """
        next_company_number = current_company_number + 1
        return next_company_number

    # handle full hyphen exception
    def str_dash_full_to_half(self, in_str: str) -> str:
        half_text = ''
        for character in in_str:
            if chr(45 + 65248).encode("utf-8") == character:
                character += "-"
            else:
                half_text += character
        return half_text

    def check_hyphen_exception(self, splited_text: list, index: int) -> str:
        splited_text[index] = " ".join(splited_text[index].split())
        splited_text[index] = splited_text[index].strip()
        #replace一a些在欄位中比較特別的符號
        splited_text[index] = splited_text[index].replace("–", "-")
        splited_text[index] = splited_text[index].replace(" - ", "-")
        splited_text[index] = splited_text[index].replace("－", "-")
        splited_text[index] = splited_text[index].replace(" ", "-")
        splited_text[index] = splited_text[index].replace("\t", "")

        return splited_text[index]

    def __gri_text_filter(self, gri_list_in_rex):
        """
        __gri_text_filter [summary] 
        filter the term from re.findall() (['1','0','2','-','1'])
        to more easier way like ['102-1','102-2'...]

        Args:
            gri_list_in_rex ([type]): [description] the term from using re.findall()

        Returns:
            [type]: [description] return the term like ['102-1','102-2'...]
        """
        splited_text = self.__get_gri_plain_text(
            gri_list_in_rex=gri_list_in_rex)

        return self.__get_numbers_part_from_gri_plain_text(splited_text)

    def __get_gri_plain_text(self, gri_list_in_rex):
        """
        __get_gri_plain_text [summary]
            get plain text splited with line (\n)W
        Args:
            gri_list_in_rex ([type]): [description]  the term from using re.findall()
        Returns:
            [type]: [description]
        """
        plain_text = ""
        empty_list = list()
        # turn the list of .findall function into more cleaner view
        for temp in range(len(gri_list_in_rex) - 1):
            plain_text = plain_text + (gri_list_in_rex[temp])
        splited_text = plain_text.splitlines()

        #remove the redundant part in the list
        for temp in range(len(splited_text) - 1):
            if splited_text[temp] == '':
                empty_list.append(temp)
        splited_text = list(
            set([i for i in splited_text if i not in empty_list]))

        no_hyphen_col = list()
        #replace the hyphens which is not offcial format
        for temp in range(len(splited_text) - 1):
            splited_text[temp] = self.check_hyphen_exception(
                splited_text, temp)

            if self.__is_contain_hyphen(splited_text[temp]):
                no_hyphen_col.append(splited_text[temp])

        with_hyphen_text = list(
            set([i for i in splited_text if i not in no_hyphen_col]))

        for temp in range(len(with_hyphen_text)-1):
            with_hyphen_text[temp] = with_hyphen_text[temp].strip()

        return with_hyphen_text

    def __get_non_numbers_part_from_gri_plain_text(self, splited_text):
        del_list = list()
        # delete some redundant data in the splited_text list
        # all we need is like 'xxx-x' term
        for temp in range(len(splited_text) - 1):
            if "-" not in splited_text[temp]:
                del_list.append(splited_text[temp])
            if "--" in splited_text[temp]:
                del_list.append(splited_text[temp])
        return del_list

    def __get_numbers_part_from_gri_plain_text(self, splited_text):
        del_list = self.__get_non_numbers_part_from_gri_plain_text(
            splited_text=splited_text)
        gri_pointers = set([i for i in splited_text if i not in del_list])
        
        return list(gri_pointers)

    def output_B_pointers(self):
        today = datetime.date.today()
        self.csv_file.to_csv(f'.\\csv_file\\{today}_gri_pointers_b.csv',
                             encoding='utf-8-sig')

    def get_gri_pointers_csv_name(self):
        return self.gri_pointers_csv_name

    def get_files_list(self):
        return self._files_list

    def get_csr_report_path(self):
        return self.csr_report_path

    def set_pattern(self, pattern):
        self.pattern = pattern

b_sheets_process = GRIPointers_B(
    csr_report_path='.\\testing_reports',
    # csr_report_path='C:\\Users\\user\\Desktop\\CSR_project\\csr_reports\\csr_reports_2020',
                                 gri_pointers_csv_name=".\\csv_file\\gri_pointers_b_frame")
b_sheets_process.set_pattern(pattern = r"[0-9-－–\s]")
b_sheets_process.init_gri_pointers_csv_file(
    b_sheets_process.gri_pointers_csv_name)
b_sheets_process.catch_gri_pointers(
    csr_report_path=b_sheets_process.get_csr_report_path(), search_term='GRI')
print(b_sheets_process.csv_file)
b_sheets_process.output_B_pointers()