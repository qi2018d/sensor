
import threading
import sqlite3
from sensor import Reader

class HistoryManager:

    class HistoryCollectThread(threading.Thread):

        def __init__(self):
            threading.Thread.__init__(self)
            self.__stop_event = threading.Event()
            self.reader = Reader()

        def stop(self):
            self.__stop_event.set()

        def __is_stopped(self):
            return self.__stop_event.is_set()

        def run(self):

            self.__create_table_if_not_exist()
            self.__loop_insert_data()

        def __create_table_if_not_exist(self):

            conn = sqlite3.connect("air_data.db")
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='air_data'")
            rows = cur.fetchall()

            # if no table exist
            if len(rows) is 0:
                print "Creating air_data table"
                cur.execute( "CREATE TABLE 'air_data' (\
                             `data_id`  INTEGER   NOT NULL    PRIMARY KEY   AUTOINCREMENT,\
                             `temp`     REAL      NOT NULL, \
                             `no2`      REAL      NOT NULL, \
                             `o3`       REAL      NOT NULL, \
                             `co`       REAL      NOT NULL, \
                             `so2`      REAL      NOT NULL,\
                             `time`     INTEGER   NOT NULL,\
                             `pm2_5`    REAL      NOT NULL)")

            conn.commit()

        def __loop_insert_data(self):

            conn = sqlite3.connect("air_data.db")
            cur = conn.cursor()
            sql = 'INSERT\
                  INTO air_data(`time`, `no2`, `o3`, `co`, `so2`, `pm2_5`, `temp`)\
                  VALUES (?, ?, ?, ?, ?, ?, ?)'

            while not self.__is_stopped():
                data = self.reader.read_all()
                print "[DB] Storing sensor data...."
                cur.execute(
                    sql,
                    (
                        data['time'],
                        data['no2'],
                        data['o3'],
                        data['co'],
                        data['so2'],
                        data['pm2_5'],
                        data['temp']
                    )
                )
                conn.commit()

            conn.close()

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
