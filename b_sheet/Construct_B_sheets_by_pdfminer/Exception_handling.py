import sys
import traceback

def get_exception(e, file):
        print(f"Unexpected error: {sys.exc_info()[0]} on {file}")
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = f'File "{fileName}", line {lineNum}, in {funcName}: [{error_class}] {detail}'
        sys_exc_info = f'cl:{cl} \n exc: {exc} \n tb:{tb}'
        print(f'Error message:======================\n{errMsg}')
        print(f'System execute info: ============================ \n {sys_exc_info}')