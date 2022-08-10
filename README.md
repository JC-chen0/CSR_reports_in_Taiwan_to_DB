# CSR_reports_in_Taiwan_to_DB
處理來自台灣三百多間企業公司的社會企業責任報告，透過處理PDF文件內容建立資料庫，以供後續文字探勘處理。


# GUI Guide
![](https://i.imgur.com/eK4V8ah.png)(圖一)

如圖一所示，將壓縮檔解壓縮後會得到兩個資料夾，分別是build以及dist:
* build: 用來打包程式用的，裡面是B表工具會使用到的套件。
* dist: 為放置工具的資料夾，實際上使用只需要點進這個資料夾即可。


![](https://i.imgur.com/1h98YRf.png)(圖二)

進入dist後，如圖二，會有一個檔案一個資料夾：
* csv_file: 用來放置輸出csv的模板，以及**處理好的CSV檔案**
> 處理好的CSV檔案會以當天的日期來命名，如圖所示![](https://i.imgur.com/SUfsa8m.png)
* crawler.exe: B表工具本體

點進crawler後，會跳出終端機以及GUI畫面：
![](https://i.imgur.com/eEuanOu.png)(終端機畫面，圖三)

> 需要注意的是，終端機會先出現把GUI畫面擋住，所以這邊需要先將終端機縮小畫面，這裡的終端機因為開發人員自訂的關係，一般來說會是全黑的。
> 
![](https://i.imgur.com/KwjnjMt.png)(GUI畫面，圖四)

進入GUI畫面後，使用步驟如下：
1. 點選選擇CSR報告位置，如圖五所示：![](https://i.imgur.com/bq9465e.png)(圖五)

CSR報告存放的資料夾畫面如圖六，直接將所有PDF檔案放入資料夾即可。
> 這邊要注意的是，資料夾內部不能有其他檔案或是其餘資料夾。
> ![](https://i.imgur.com/5vNxvPX.png)(圖六)


2. 選擇完資料夾後，畫面如圖七所示，原先空白的格子會有路徑產生，並且右側的輸出B表CSV可以點選了。
![](https://i.imgur.com/bbi6z19.png)(圖七)

3. 點選輸出B表CSV檔案，可以看到底下的bar開始跑動，以及剛剛開啟程式的終端機開始在處理資料，處理完成後會跳出提示。
![](https://i.imgur.com/GExMTpN.png)

4. 回到dist > csv_file的資料夾，裡面會有今日日期的CSV檔案，如圖所示:
![](https://i.imgur.com/nAk8804.png)

## Notice

1. 需要注意的是目前版本因為讀取的PDF檔案較多，讀取途中如果需要關掉程式，後端程式會無法關閉，建議使用工作管理員或是在其無法回應時強制關閉。
2. 如路徑選擇錯誤，沒有資料的情況下點選輸出按鈕，可以直接關掉程式重新再點選一次
3. 目前因為怕每一台電腦的效能不同，所以Thread只開了一個，如果使用完程式還想要重新使用，請重新開啟使用。

# files

## Construct_B_sheets_by_pdfminer
### packages:
存放一些簡單的小程式：
* Construct_B_sheets.py: 用來建立 csv_file內的gri_pointers_b_frame.csv以用來進行B表的處理。
* Exception_handling.py: 處理例外
* Judging_csr_reports_level.py: 簡單分級，將報告處理的層級、優先程度進行分級，方便開發人員判別哪些是好開發的
* pointers_transfer.py: 轉換指標

### csv_file:
存放輸出資料以及b表CSV檔frame處

### crawler.py
主要運行的程式，內含B表處理邏輯以及GUI介面設定，運行方式為：
```python=
python crawler.py 
```
### main.py
Depreciated
目前已無使用，可從這裡開始進行修改，建立整套B表服務的Script。

# Required library
PyMuPDF (import fitz)
Pandas
Tkinter
threading
multiprocessing

此處沒有使用requirement.txt的原因在於視不同安裝方式，例如pip或是conda會有不同的裝法，建議可以直接使用pip安裝
# 更新日誌

22/08/10
整理目前現有所使用的檔案
增加簡單的GUI提供使用者使用

22/01/16 By JC
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
