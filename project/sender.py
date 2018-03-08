import json
import threading
import time
from db_manager import DBManager


class Sender:

    def __init__(self, active_handles):
        self.lock = threading.Lock()
        self.active_handlers = active_handles
        self.wait = 50 #ms
        self.error_wait = 100#ms

    def send(self, data):

        self.lock.acquire()
        for handler in self.active_handlers:
            try:
                handler.send(json.dumps(data))
                time.sleep(self.wait/1000)
            except:
                print "Error while sending data : " + str(data)
                time.sleep(self.error_wait/1000)

        self.lock.release()

    def send_air_history_from(self, timestamp):

        data = DBManager.get_air_data_from(timestamp)
        print "Sending " + str(len(data)) + " historical data from " + str(timestamp)

        chunk_size = 5

        # chop chop chop in chunk with size of chunk_size
        if data is not None:
            data_chunks = [data[i:i + chunk_size] for i in xrange(0, len(data), chunk_size)]
            for chunk in data_chunks:
                self.send({'type': 'historical', 'data': chunk})
