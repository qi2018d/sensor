import os
import csv
import sqlite3
import threading

class BTArchive(threading.Thread):
    def __init__(self, buffer_size=1024):
        threading.Thread.__init__(self)
        self.DB_path = '/home/udooer/Database/C_UDOO_DB.db'
        self.CSV_path = '/home/udooer/csv/C_UDOO_data.csv'
        self.all_CSV_path = '/home/udooer/csv/C_UDOO_all_data.csv'
        self.buffer_size = buffer_size ##one time sending able to 1024 byte
        self.WRLock = threading.Lock()
        self.all_csv_sending_flag = False
        self.csv_sending_flag = False
        self.running = True
        self.SERVER = None

    def run(self):
        print "Archive Thread start"
        while self.running:
            if self.csv_sending_flag == True:
                self.create_csv('data')
                print "sucess send csv file"

            if self.all_csv_sending_flag == True:
                self.create_all_csv('data')
                print "sucess send all csv file"

    ##create&send csv file per 3600 sec(1hour)
    def create_csv(self,table_name):
        db_conn = sqlite3.connect(self.DB_path)
        cur = db_conn.cursor()
        with open(self.CSV_path, 'w') as csv_file:
            cur.execute('SELECT C_TIME,TEMP,PM25,CO,NO2,SO2,O3 FROM (SELECT * FROM {tn} ORDER BY NUM DESC LIMIT 3600) ORDER BY NUM ASC'.format(tn=table_name))
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(cur)
        f = open(self.CSV_path, "rb")
        CSV_byte = f.read(self.buffer_size)
        self.SERVER.send("start_CSV")
        CSV_byte = str(CSV_byte)
        size = len(CSV_byte)
        while CSV_byte:
            self.SERVER.send(CSV_byte)
            CSV_byte = f.read(self.buffer_size)
            CSV_byte = str(CSV_byte)
            if( (size > len(CSV_byte)) and (len(CSV_byte) != 0) ) :
                CSV_byte='&'+CSV_byte
        self.SERVER.send("end_CSV")
        f.close()
        self.csv_sending_flag = False

    def create_all_csv(self,table_name):
        db_conn = sqlite3.connect(self.DB_path)
        cur = db_conn.cursor()
        with open(self.all_CSV_path, 'w') as csv_file:
            cur.execute('SELECT C_TIME,TEMP,PM25,CO,NO2,SO2,O3 FROM {tn} ORDER BY NUM ASC'.format(tn=table_name))
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(cur)
        f = open(self.all_CSV_path, "rb")
        CSV_byte = f.read(self.buffer_size)
        self.SERVER.send("start_last_CSV")
        CSV_byte = str(CSV_byte)
        size = len(CSV_byte)
        while CSV_byte:
            self.SERVER.send(CSV_byte)
            CSV_byte = f.read(self.buffer_size)
            CSV_byte = str(CSV_byte)
            if( (size > len(CSV_byte)) and (len(CSV_byte) != 0) ) :
                CSV_byte='&'+CSV_byte
        self.SERVER.send("end_last_CSV")
        f.close()
        self.all_csv_sending_flag = False

