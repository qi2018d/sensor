import logging
from BTSensorDevice import BTSensor
from BTSocketServer import BTSocketServer
from BTSensorDevice import BTSensorReader_thr

##global variable
logging.basicConfig(level=logging.INFO) ##using import BT*
Flag_connec = False ##This is a flag to check the server is alive.

## initialize 6 sensors list
def func_Sensors():
    return [BTSensor(id=0,name="Temp"),
            BTSensor(id=1,name="PM25"),
            BTSensor(id=2,name="CO"),
            BTSensor(id=3,name="NO2"),
            BTSensor(id=4,name="SO2"),
            BTSensor(id=5,name="O3")]

sensors = func_Sensors()
reader = BTSensorReader_thr(sensors=sensors)
reader.start()

#BT cmd(setup)
while True:
    try:
        ##when starting UDOO , start server
        if Flag_connec != True:
            server = BTSocketServer()
            server.start()
            server.wait()
            Flag_connec = True

        ##when connected bluetooth connection with application
        else:
            data = server.recv()
            recv_str = data.partition(",")
            print("received [%s]" % data)

            ##if receive string 'start', start sending
            if recv_str[0] == "start":
                print("Start sending data...")
                if recv_str[2] != "":
                    reader.timectl = int(recv_str[2])
                reader.SERVER = server
                reader.sensing_flag = True
                reader.send_req = True

            ##if receive string 'stop', stop sending
            elif recv_str[0] == "disconnect":
                print("Stop sending data...")
                reader.send_req = False
                reader.csv_req = True
                reader.send_flag = 0
                reader.csv_flag = 0

    except IOError:
        reader.send_flag = 0
        reader.csv_flag = 0
        reader.send_req = False
        Flag_connec = False
        server.stop()

