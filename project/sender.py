import json
import threading
from db_manager import DBManager

class Sender:

    class DataEncoder(json.JSONEncoder):
        def encode(self, obj):
            if isinstance(obj, float):
                return format(obj, '.2f')
            return json.JSONEncoder.encode(self, obj)

    def __init__(self, active_handles):
        self.lock = threading.Lock()
        self.active_handlers = active_handles

    def send(self, data):

        self.lock.acquire()
        for handler in self.active_handlers:
            json_string = json.dumps(data, cls= self.DataEncoder)
            handler.send(json_string)
        self.lock.release()

    def send_air_history_from(self, timestamp):

        chunk_size = 5

        data = DBManager.get_air_data_from(timestamp)

        # send historical data if exists
        if data is not None:
            data_chunks = [data[i:i + chunk_size] for i in xrange(0, len(data), chunk_size)]

            for chunk in data_chunks:
                self.send({'type': 'historical', 'data': chunk})

    def __format(self, data):
        pass