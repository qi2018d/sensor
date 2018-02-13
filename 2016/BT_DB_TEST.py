from BTSocketServer import BTSocketServer
import threading
import logging
import random
import sqlite3
import time
import json
import collections

##global flags variable
Flag_connec = False
thr_start =False
create_flag = False

##BT connection
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BT_DB_Thread(threading.Thread):
    def __init__(self,server,n):
        threading.Thread.__init__(self)
        self.server = server #server(BT)
        self.n = n # n sec


    ## insert random value in list(output)
    def read_sensor(self):
        CO2 = random.randint(1,100)
        NO2 = random.randint(1,100)
        SO2 = random.randint(1,100)
        O3 = random.randint(1,100)
        PM25 = random.randint(1,100)
        TEMP = random.randint(20,40)
        CT = int(time.time())

        return [ CO2, NO2, SO2, O3, PM25, TEMP, CT ]

    ## send list(outputs) to android using bluetooth
    def send_to_BT(self,outputs):
        self.server.send(str(outputs) +'\n')

    ## create table and insert data in table (not yet create table)
    ## OR only insert data in Table (alreay create table)
    def write_to_DB(self,outputs,table_name):
    #with open('/Users/suhyeunchoi/Desktop/python/json/db_test.json', 'w') as json_test:

        ##DB connection
        self.conn = sqlite3.connect("db_test.db")
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        ##create table and insert data
        global create_flag

        if create_flag == False: #local variable 'create_flag' referenced before assignment
            self.cur.execute('CREATE TABLE {tn} \
                        (data_num integer primary key autoincrement, \
                        CO2 integer, \
                        NO2 integer, \
                        SO2 integer, \
                        O3 integer, \
                        PM25 integer, \
                        TEMP integer, \
                        C_TIME integer)'.format(tn=table_name))

            self.cur.executemany('INSERT INTO {tn} VALUES (CO2,NO2,SO2,O3,PM25,TEMP,C_TIME)'.format(tn=table_name), outputs)
            create_flag = True

        ##only insert data
        elif create_flag == True:
            self.cur.executemany('INSERT INTO {tn} VALUES (CO2,NO2,SO2,O3,PM25,TEMP,C_TIME)'.format(tn=table_name), outputs)

        self.conn.commit()

        #cur.execute("select * from data")  #much data read?
        #data = cur.fetchall()
    #rows = [ dict(rec) for rec in data ]
    #json_test.write(json.dumps(rows, indent = 4))

    def run(self) :
        outputs = list()
        while thr_start:
            output = self.read_sensor()
            outputs.append(output)

            if len(outputs) == self.n:
                self.send_to_BT(outputs)
                self.write_to_DB(outputs, 'data_test3')
                outputs = list()

            time.sleep(1)


        cur.close()
##BT cmd(setup), main process
while True:
    try:
        if Flag_connec != True:
            server = BTSocketServer()
            server.start()
            server.wait()
            Flag_connec = True

        else:
            data = server.recv()
            if len(data) == 0: continue
            print("received [%s]" % data)
            if(data == "start"):
                print("received [%s]" % data)
                if thr_start != True:
                    thr_start = True  ## I want resurrection of the thread, but I don't know anyway
                    BT_DB_process = BT_DB_Thread(server,3)
                    BT_DB_process.start()

            elif(data == "stop"):
                print("received [%s]" % data)
                thr_start = False
                Flag_connec = False

    except IOError:
        server.stop()
        thr_start = False
        Flag_connec = False


server.close()

