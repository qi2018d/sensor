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
            handler.send(json.dumps(data, cls= self.DataEncoder))
        self.lock.release()

    def send_air_history_from(self, timestamp):

        data = DBManager.get_air_data_from(timestamp)
        chunk_size = 5

        # chop chop chop in chunk with size of chunk_size
        if data is not None:
            data_chunks = [data[i:i + chunk_size] for i in xrange(0, len(data), chunk_size)]

            for chunk in data_chunks:
                self.lock.acquire()
                for handler in self.active_handlers:
                    handler.send(json.dumps({'type': 'historical', 'data': chunk}, cls=self.DataEncoder))
                self.lock.release()
