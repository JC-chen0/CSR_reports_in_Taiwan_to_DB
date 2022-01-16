# CSR_reports_in_Taiwan_to_DB
處理來自台灣三百多間企業公司的社會企業責任報告，透過處理PDF文件內容建立資料庫，以供後續文字探勘處理。
***



### 更新日誌

21/01/16 By JC
目前可使用功能：
版本1.0目前已經可以將文字版本的GRI指標對照表，內部所有的揭露指標都可以抓到了。

* [crawler.ipynb] 利用Jupyter來測試
* [crawler.py] [main.py] 最主要之後用來打包是好用的
* [packages] 為一些簡單的function寫在裡面，到時候會再整理一下crawler內部的function名稱


11/23
目前可使用功能：

db_operation.py :可簡單使用程式擷取資料
Construct_B_sheets_by_pdfminer : 可找到GRI pointers揭露指標的table，並且已揭露項目輸出成excel表。 

尚未解決問題：
* 圖片掃描的CSR報告目前尚未能處理。
* 目前程式判斷是否揭露的標準是透過爬取GRI揭露表格來偵測是否揭露，然而有些公司具有不一樣的格式 (e.g. 將所有指標列出然後標註是否揭露)，造成判斷的依據有問題。
* 程式目前仍有些問題。
