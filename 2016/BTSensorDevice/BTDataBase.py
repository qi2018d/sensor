import json
import sqlite3
import collections

class BTDataBase():
    ##initialize DB and CSV path
    def __init__(self):
        self.DB_path = '/home/udooer/Database/C_UDOO_DB.db'
        self.CSV_path = '/home/udooer/csv/C_UDOO_data.csv'

    ##query of create table
    def create_table(self,table_name):
        db_conn = sqlite3.connect(self.DB_path)
        cur = db_conn.cursor()
        cur.execute('CREATE TABLE {tn} \
                        (NUM integer PRIMARY KEY AUTOINCREMENT ,C_TIME integer,TEMP integer,PM25 REAL, \
                        CO REAL, NO2 REAL, SO2 REAL,O3 REAL)'.format(tn=table_name))
        db_conn.commit()

    ##query of delete table
    def delete_table(self,table_name):
        db_conn = sqlite3.connect(self.DB_path)
        cur = db_conn.cursor()
        cur.execute('DROP TABLE {tn}'.format(tn=table_name))
        db_conn.commit()

    ##query of insert data(data_list) to table
    def insert_data(self,table_name,data_list):
        db_conn = sqlite3.connect(self.DB_path)
        cur = db_conn.cursor()
        cur.execute('INSERT INTO {tn} (C_TIME, TEMP, PM25, CO, NO2, SO2, O3) VALUES(?,?,?,?,?,?,?)'.format(tn=table_name), data_list)
        db_conn.commit()

    ##query of search latest data in table and return json format data
    def select_real_data(self,table_name):
        db_conn = sqlite3.connect(self.DB_path)
        db_conn.row_factory = sqlite3.Row
        cur = db_conn.cursor()
        cur.execute('SELECT C_TIME,TEMP,PM25,CO,NO2,SO2,O3 FROM {tn} ORDER BY NUM DESC limit 1'.format(tn=table_name))
        data = cur.fetchall()
        rows = [ dict(rec) for rec in data ]
        return json.dumps(rows)

