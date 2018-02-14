
import sqlite3

class DBManager:

    db_name = "air_data.db"

    @staticmethod
    def insert_air_data(data):

        DBManager.__create_air_table_if_not_exist()

        conn = sqlite3.connect(DBManager.db_name)
        cur = conn.cursor()
        cur.execute(
            'INSERT\
                  INTO air(`time`, `no2`, `o3`, `co`, `so2`, `pm2_5`, `temp`)\
                   VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                data['time'],   data['no2'],    data['o3'],     data['co'],
                data['so2'],    data['pm2_5'],  data['temp']
            )
        )
        conn.commit()
        conn.close()

    @staticmethod
    def insert_aqi_data(data):

        DBManager.__create_aqi_table_if_not_exist()

        conn = sqlite3.connect(DBManager.db_name)
        cur = conn.cursor()
        cur.execute(
            'INSERT\
                INTO aqi(`time`, `no2`, `o3`, `co`, `so2`, `pm2_5`, `temp`)\
                VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                data['time'],   data['no2'],    data['o3'],     data['co'],
                data['so2'],    data['pm2_5'],  data['temp']
            )
        )
        conn.commit()
        conn.close()

    @staticmethod
    def insert_history_data(data):
        DBManager.__create_aqi_table_if_not_exist()

        conn = sqlite3.connect(DBManager.db_name)
        cur = conn.cursor()
        cur.execute(
            'INSERT\
                INTO aqi(`time`, `no2`, `o3`, `co`, `so2`, `pm2_5`, `temp`)\
                VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                data['time'], data['no2'], data['o3'], data['co'],
                data['so2'], data['pm2_5'], data['temp']
            )
        )
        conn.commit()
        conn.close()


    @staticmethod
    def get_data(period):



    @staticmethod
    def __create_air_table_if_not_exist():

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

    @staticmethod
    def __create_aqi_table_if_not_exist():

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

        conn.close()

    @staticmethod
    def __create_history_table_if_not_exist():

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


