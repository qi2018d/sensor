import json
import threading

json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')

class Sender:

    lock = threading.Lock()

    def __init__(self, active_handles):
        self.active_handlers = active_handles

    def send(self, data):
        Sender.lock.acquire()
        for handler in self.active_handlers:
            handler.send(json.dumps(data))
        Sender.lock.relese()

'''
    def run(self):

        while not self.__is_stopped():

            data = {'type': 'real-time', 'data': self.reader.read_all()}
            data_string = json.dumps(data, sort_keys=True)
            print "Sending sensor data to android....."

            try:
                self.bt_handler.send(data_string)

            except BluetoothError as e:
                print e.message
                break
'''
