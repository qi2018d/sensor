
import threading
import sqlite3
from sensor import Reader

class HistoricalProcessor(threading.Thread):

    '''
    Store sensor data every second while running
    '''


    def __init__(self):
        super(HistoricalProcessor, self).__init__()

        self._stop_event = threading.Event()
        self.reader = Reader()


    def stop(self):
        self._stop_event.set()

    def __is_stopped(self):
        return self._stop_event.is_set()

    def run(self):

        conn = sqlite3.connect("air_data.db")
        cur = conn.cursor()

        self.create_table_if_not_exist(conn, cur)

        sql = 'INSERT INTO air_data(`time`, `no2`, `o3`, `co`, `so2`, `pm2_5`, `temp`)\
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


    def create_table_if_not_exist(self, conn, cur):

        check_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='air_data'"
        create_sql = "CREATE TABLE 'air_data' ( `data_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `temp` REAL NOT NULL, `no2` REAL NOT NULL, `o3` REAL NOT NULL, `co` REAL NOT NULL, `so2` REAL NOT NULL, `time` INTEGER NOT NULL, `pm2_5` REAL NOT NULL)"

        cur.execute(check_sql)
        rows = cur.fetchall()

        if len(rows) is 0:
            cur.execute(create_sql)
            conn.commit()