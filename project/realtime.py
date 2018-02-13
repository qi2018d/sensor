import threading
from sensor import Reader
import json
import sqlite3
from bluetooth import BluetoothError

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')


class RealtimeProcessor(threading.Thread):

    def __init__(self, bt_handler):
        super(RealtimeProcessor, self).__init__()

        self._stop_event = threading.Event()

        self.bt_handler = bt_handler
        self.reader = Reader()


    def stop(self):
        self._stop_event.set()

    def __is_stopped(self):
        return self._stop_event.is_set()

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
