
import threading
import sqlite3
from reader_thread import ReaderThread

class HistoryManager:

    class HistoryCollectThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.__stop_event = threading.Event()
            self.reader = ReaderThread()

        def stop(self):
            self.__stop_event.set()

        def __is_stopped(self):
            return self.__stop_event.is_set()

        def run(self):





    def __init__(self):
        self.saver = None

    def start_saving(self):
        if self.saver is None:
            self.saver = self.HistoryCollectThread()
            self.saver.start()

    def stop_saving (self):
        if self.saver is not None:
            self.saver.stop()
            self.saver.join()
            self.saver = None

        return {}

    def is_saving(self):
        return True if self.saver is not None else False

    def get_saved_data(self):

        conn = sqlite3.connect("air_data.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM air_data")
        data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

        cur.execute("DELETE FROM air_data")
        conn.commit()

        return data
