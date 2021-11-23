"""
Created on Wed Sep 09 15:10:28 2021

@author: Joe.Chen mail: jyou.chen0@gmail.com
"""

import pandas as pd
import numpy as np
import mysql.connector
import argparse
import socket
import select

class db_opreation:
    def __init__(self):
        self.host = ''
        self.database = ''
        self.user = ''
        self.password = ''
        self.port = ''
        self.connection = ''
        self.db_df = ''
        self.TIMEOUT=10
        self.IFACE='127.0.0.1'
        self.PORT=4000
        self.DEBUG=False
        self.myList = []
        self.old = ""

    def connect_to_DB(self, host, database, user, password, port):
        try:
            # 連接 MySQL/MariaDB 資料庫
            self.connection = mysql.connector.connect(
                host=self.host,  # 主機名稱
                database=self.database,  # 資料庫名稱
                user=self.user,  # 帳號
                password=self.password,  # 密碼
                port=self.port)

            if self.connection.is_connected():
                # 顯示資料庫版本
                db_Info = self.connection.get_server_info()
                print("資料庫版本：", db_Info)
                # 顯示目前使用的資料庫
                cursor = self.connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("目前使用的資料庫：", record)

        except Exception as e:
            print("資料庫連接失敗：", e)

    def disconnect_to_DB(self):
        if (self.connection.is_connected()):
            self.connection.close()
            print("資料庫連線已關閉")

    def process_raw_data(self):
        """
        process_raw_data [summary]
        TODO: Input the raw data, process the unicode part using functions
        """
        pass

    def turn_unicode_to_plain_text(self):
        """
        turn_unicode_to_plain_text [summary]
        TODO: 
        1. Detect the unicode part
        2. Turn unicode part to plain text 
        """
        pass

    def get_csrone_reports_db_entities(self) -> pd.DataFrame:
        db_df = pd.read_sql(
            "SELECT * FROM csrone_rat_reports WHERE status_id = 4;",
            con=self.connection,
            encoding='utf-8')
        print("Exporting from database ...")
        print(db_df)
        return db_df
        # db_df.to_excel("csrone_reports_raw_data.xlsx", encoding='utf-8-sig')

    def show_table_schema(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f'describe {table_name};')
        print(f'Now showing schema of {table_name}')
        for i in cursor:
            print(i)
        cursor.close()

    def show_all_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('show tables;')
        print(f'Now Showing tables:')
        for temp in cursor:
            print(temp)
        cursor.close()

    def show_all_entities(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        for temp in cursor:
            print(temp)
        cursor.close()

    # getter and setter

    def set_host(self, n_host):
        self.host = n_host

    def set_database(self, n_database):
        self.database = n_database

    def set_user(self, n_user):
        self.user = n_user

    def set_password(self, n_password):
        self.password = n_password

    def set_port(self, n_port):
        self.port = n_port

    def set_db_df(self, n_db_df: pd.DataFrame):
        self.db_df = n_db_df

    def get_db_df(self) -> pd.DataFrame:
        return self.db_df

    def get_host(self):
        return self.host

    def get_database(self):
        return self.database

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_port(self):
        return self.port
    

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="139.162.83.224")
parser.add_argument("--database", type=str, default="csrone_rat")
parser.add_argument("--user", type=str, default="csrone_rat_reader")
parser.add_argument("--password", type=str, default="TixRl1XwGmUOhRcr")
parser.add_argument("--port", type=int, default="3306")

parser.add_argument(
    "--export_csr_reports",
    action='store_true',
    help="Export the entities in csrone_rat_reports into .xlsx")

parser.add_argument("--show_table_schema",
                    type=str,
                    nargs='+',
                    help="Show selected table schema.")

parser.add_argument("--show_all_tables",
                    action='store_true',
                    help="Show all the table in the db.")

parser.add_argument("--show_all_entities",
                    type=str,
                    nargs='+',
                    help='Show all the entities in selected table')

parser.add_argument("--exit", nargs='?', help='disconnect')

args = parser.parse_args()
db_opreation = db_opreation()
db_opreation.set_host(args.host)
db_opreation.set_database(args.database)
db_opreation.set_user(args.user)
db_opreation.set_password(args.password)
db_opreation.set_port(args.port)

db_opreation.connect_to_DB(host=db_opreation.get_host(),
                           database=db_opreation.get_database(),
                           user=db_opreation.get_user(),
                           password=db_opreation.get_password(),
                           port=db_opreation.get_port())

if args.export_csr_reports:

    print("Processing the unicode parts ... ")
    print("Exporting completed, please check the .xlsx file in the folder.")

if args.show_table_schema:
    db_opreation.show_table_schema(args.show_table_schema[0])

if args.show_all_tables:
    db_opreation.show_all_tables()

if args.show_all_entities:
    db_opreation.show_all_entities(args.show_all_entities[0])

if args.exit:
    db_opreation.disconnect_to_DB()
    