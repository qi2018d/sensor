import threading
import time
from db_manager import DBManager


class AQIThread(threading.Thread):

    def __init__(self, sender):
        threading.Thread.__init__(self)
        self.sender = sender
        self.interval =

    def run(self):

        while True:

            self.calculate_aqi()

            DBManager.insert_aqi_data(data)
            self.sender.send({"type": "real-time", "data":data})

    def calculate_aqi(self, data):
