import os
import time
import sqlite3
import datetime
import random
import threading
from BTArchive import BTArchive
from BTDataBase import BTDataBase

import random ### delete to do this line ###

class BTSensorReader_thr(threading.Thread):
    def __init__(self,sensors=None,
                 reading_interval=0.4,
                 sending_interval=3,
                 CSV_interval=3600):
        threading.Thread.__init__(self)
        CO = [1.4, 1.03, 0.85, 0.62, 0.3, 0.03, -0.25, -0.48, 346,274,276]
        NO2 = [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2, 220,260,207]
        SO2 = [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75, 300,294,300]
        O3 = [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 414,400,256]
        self.SE = [CO, NO2, SO2, O3]
        self.reading_interval = reading_interval
        self.sending_interval = sending_interval
        self.CSV_interval = CSV_interval
        self.DB_path = "/home/udooer/Database/C_UDOO_DB.db"
        self.BTDB = BTDataBase()
        self.WRLock = threading.Lock()
        self.csv_sender = BTArchive()
        self.sensor_list = list()
        self.sensors = sensors
        self.running = True
        self.sensing_flag = False
        self.send_req = False
        self.csv_req = False
        self.SERVER = None
        self.d_time = None
        self.send_flag = 0
        self.csv_flag = 0
        self.timectl = 0

    def run(self):
        print "Sensing & Real Thread start"
        self.csv_sender.start()
        while self.running:
            if self.sensing_flag:
                ##insert sensor data into list(sensor_list)
                self.sensing()

                ##time syncronize
                self.d_time = datetime.datetime.now()
                u_time = int(time.mktime(self.d_time.timetuple()))
                if (self.timectl != 0):
                    self.time_err = abs(self.timectl - u_time)
                    self.timectl = 0
                u_time = u_time + self.time_err - 25200
                self.sensor_list.insert(0,u_time + 25200)
                print time.ctime(u_time)

                if (int(self.d_time.strftime("%f"))<400000):
                    time.sleep(self.reading_interval)

                ## insert data(sensor_list) into DB
                self.write_database()
                ##sending Realdata or csv file
                self.sendig_data()

    def sensing(self):
       # PT = self.sensors[0].read()
	PT = random.uniform(22,28)
        PM = self.sensors[1].read()
        self.sensor_list = [PT, PM] ##insert time and PM data into list(sensor_list)

        ##Calculation airSensor Data
        for airSensor in xrange(2,6):
            result = self.sensor_calculation(self.sensors[airSensor].read(),self.SE[airSensor-2][self.temp_set(PT)],airSensor-2)
            if result < 0:
                result = 0
            self.sensor_list.append(round(result,1))  ##insert CO, NO2, SO2, O3 data into list(sensor_list)

    def write_database(self):
        self.WRLock.acquire()
        ##if already create database
        if os.path.exists(self.DB_path):
            self.BTDB.insert_data('data',self.sensor_list)

        ##if not create database
        else:
            self.BTDB.create_table('data')
            self.BTDB.insert_data('data',self.sensor_list)
        self.WRLock.release()

    def sendig_data(self):
        ##when receive start message sending Realdata(3sec) & csv file(1hour)
        if (self.send_req == True):
            self.send_flag += 1
            self.csv_flag += 1

            ##sending csv file per 3600 sec(1hour)
            if (self.csv_flag == self.CSV_interval):
                self.send_flag = 0
                self.csv_flag = 0
                self.csv_sender.SERVER = self.SERVER
                self.csv_sender.csv_sending_flag = True

            ##sending Realdata per 3 sec
            if (self.send_flag == self.sending_interval):
                self.send_flag = 0
                self.WRLock.acquire()
                self.SERVER.send(self.BTDB.select_real_data('data'))
                self.WRLock.release()

        ##when receive stop message sending all_csv file
        elif (self.send_req == False):
            if(self.csv_req == True):
                self.csv_sender.SERVER = self.SERVER
                self.csv_sender.all_csv_sending_flag = True
                self.csv_req = False

    def temp_set(self, TEMP):
        index = 0
        temp_range = [-30,-20,-10,0,10,20,30,40]
        Min = abs(TEMP - temp_range[0])
        for x in xrange(1,8):
            if Min >= abs(TEMP - temp_range[x]):
                Min = abs(TEMP - temp_range[x])
                index = x
        return index

    def sensor_calculation(self,WA,n,SE_id):
        PPB = ((WA[0] - self.SE[SE_id][8]) - n*(WA[1] - self.SE[SE_id][9]))/self.SE[SE_id][10]
        return PPB

