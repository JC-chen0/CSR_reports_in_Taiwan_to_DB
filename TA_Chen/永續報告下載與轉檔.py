"""
Created on Wed May 20 23:27:28 2020

@author: Benson.Huang
@edited: Zoe.Chen
"""

#0.建議將此code另存避免誤改，相關檔案也建議存放於本地端路徑操作
#0-1.若有必要更動原始code記得"ctrl+save"
#0-2. 先跑這9行資料
import pandas as pd
import urllib
from urllib.request import urlretrieve
from pdf2image import convert_from_path
from time import sleep
import os
import glob
import tempfile

from pdf2image import convert_from_path


#1. 將公開資訊觀測站的資料複製貼上csv檔，並經過VBA處理，路徑需調整
#1-1.第二次之後從公開資訊觀測站上找的企業資訊，需先進行比對刪除前幾次已找過的，再讓CODE找沒找過的就可以
#1-2.轉VBA請參考使用手冊，路徑>> "永續報告分析專案 - 2021\10. 專案交接資料\01. 報告書下載\使用手冊.pdf"
companyData_path ="C:\\Users\\admin\\Desktop\\PY\\0817_報告測試.csv"
# companyData_path =".\0818報告書_測試.csv"
#2. 公司代號與公司名稱對應的CSV檔，路徑需調整
companyName_path = "C:\\Users\\admin\\Desktop\\PY\\company_name&number.csv"

#3. 報告書出版年
year = "2021"

#4. 儲存報告書pdf檔的路徑，路徑需調整
download_path = "C:\\Users\\admin\\Desktop\\PY\\\pdf\\"

#5. 設定表格，表頭標題請避免任意更動
title = ["公司代號", "公司名稱", "英文簡稱", "申報原因", "產業類別", "報告書內容涵蓋期間", "編製依循準則", "第三方驗證驗證單位", "第三方驗證單位名稱", "第三方驗證採用標準", "公司網站報告書相關資訊", "英文版企業社會責任報告書網址", "企業社會責任報告書", "上傳日期", "企業社會責任報告書(修正後版本)", "上傳日期(修正後版本)", "報告書聯絡資訊", "備註", "CSR報告超連結", "公司完整名稱","統一編號"]
data = pd.read_csv(companyData_path, header = 3, names = title, encoding = 'cp950')

#6. 匯入公司代號與公司名稱對應的csv檔
companyName = pd.read_csv(companyName_path, encoding = 'utf-8')

#7. 將對應完整公司名稱填入表格 
for i in range(len(data["公司代號"])):
    for j in range(len(companyName["公司代號"])):
        if str(data["公司代號"][i]) == companyName["公司代號"][j]:
            data.iloc[i,19] = companyName["公司名稱"][j]
            break

#8. 將統一編號填入對應的表格
for i in range(len(data["公司代號"])):
    for j in range(len(companyName["公司代號"])):
        if str(data["公司代號"][i]) == companyName["公司代號"][j]:
            data.iloc[i,20] = companyName["_統一編號"][j]
            break

#9. 清楚表格中可能的錯誤
data['統一編號'] = data['統一編號'].str.replace('\t', '')


#10-1. 讀取超連結並下載檔案，重新命名，調整range數值，range括號內數字確認本次要下載的範圍
for i in range(0,5):
    url = data["CSR報告超連結"][i]
    fileName = download_path + year + data["統一編號"][i] +".pdf"
    urllib.request.urlretrieve(url,fileName)
    sleep(10) #休息是為了走更長遠的路 秒數可彈性調整

#10-2. 如果懶得確認，就直接跑一輪
for i in range(len(data["CSR報告超連結"])):
    url = data["CSR報告超連結"][i]
    fileName = download_path + year + data["統一編號"][i] +".pdf"
    urllib.request.urlretrieve(url,fileName)
    sleep(10)
    break
    

#11. 先把PDF的路徑叫進來，路徑需調整
pdf_dir = "C:\\Users\\admin\\Desktop\\PY\\\pdf\\"
os.chdir(pdf_dir)

#12. 開始轉換PDF成JPG
for pdf_file in glob.glob(os.path.join(pdf_dir, "*.pdf")):
    images_from_path = convert_from_path(pdf_file, output_folder='C:\\Users\\admin\\Desktop\\PY\\jpg\\', last_page=1, first_page =0)
    base_filename  =  os.path.splitext(os.path.basename(pdf_file))[0] + '.jpg'     
    save_dir = 'C:\\Users\\admin\\Desktop\\PY\\jpg\\'
    for page in images_from_path:
        page.save(os.path.join(save_dir, base_filename), 'JPEG')
        sleep(5) #休息是為了走更長遠的路
        
#13. 移除其餘的暫存.ppm
n = 0
for root, dirs, files in os.walk(r'C:\\Users\\admin\\Desktop\\PY\\jpg\\'):
    for name in files:
        if(name.endswith(".ppm")):
            n += 1
            print(n)
            os.remove(os.path.join(root, name))



#14. 匯出資料(不一定用得到)
data.to_csv("C:\\Users\\admin\\Desktop\\PY\\Download_0817.csv", encoding = "UTF-8")

#其他資訊
conda config --add channels conda-forge
conda install poppler
conda search poppler --channel conda-forge
# Import libraries
from pdf2image import convert_from_path
from os import listdir
from os.path import isfile, join
import sys

"""
Created on Wed May 20 23:27:28 2020

@author: Benson.Huang
@edited: Zoe.Chen
"""