import threading
import time
from bluetooth import *
import random
thr_stop = True

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
                    )

class BT_send_Thread(threading.Thread):
    def __init__(self,c_sock):
        threading.Thread.__init__(self)
        self.c_sock = c_sock
    def run(self):
        while thr_stop:
            #raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            #scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            raw = random.randint(4,5)
            scale = random.randint(5,8)
            vout = raw * scale
            v20 = 345
            #temp = vout - v20 + 20
            temp = vout
            sent = self.c_sock.send("temperature = {0:.1f} C ".format(temp) + time.ctime() + "\n")
            print("%d bytes sent" % sent)
            time.sleep(1)

print("Waiting for connection on RFCOMM channel %d" % port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
try:
    thr_check = 1
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
        if (data == "start"):
            if (thr_check == 1):
                BT_send_process = BT_send_Thread(client_sock)
                BT_send_process.start()
                thr_check -= 1

        elif (data == "stop"):
            thr_stop = False
            thr_check = 1

except IOError:
    print("disconnected")
    client_sock.close()
    server_sock.close()


