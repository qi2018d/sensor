import threading
import time

from db_manager import DBManager


class AQIThread(threading.Thread):

    def __init__(self, sender):
        threading.Thread.__init__(self)
        self.sender = sender

        self.wait = 3 #sec
        self.interval = 20 #sec
        self.period = 120 #sec

    def run(self):

        time.sleep(self.wait)

        while True:
            aqi = self.calculate_aqi()
            # DBManager.insert_aqi_data(data)
            self.sender.send({"type": "aqi", "data": aqi})

            time.sleep(self.interval)

    def calculate_aqi(self):
        data_set = DBManager.get_air_data_from(time.time() - self.period)

        aqi = {}
        for key in {'o3', 'co', 'so2', 'no2', 'pm2_5'}:

            avg = 0
            for i in range(len(data_set)):
                avg += data_set[i][key]
            avg /= len(data_set)

            aqi[key] = self.__get_aqi(key, avg)

        aqi["time"] = int(time.time())
        print "AQI of " + str(len(data_set)) + " data  "  + str(aqi)
        return aqi

    def __get_aqi(self, key, concentration):

        table = {
            "criteria": {
                "o3":       [0,    55,    71,    86,   106,   405,   505,   605],
                "co":       [0,   4.5,   9.5,  12.5,  15.5,  30.5,  40.5,  50.5],
                "so2":      [0,    36,    76,   186,   305,   605,   805,  1005],
                "no2":      [0,    54,   101,   361,   650,  1250,  1650,  2050],
                "pm2_5":    [0,  12.1,  35.5,  55.5, 150.5, 250.5, 350.5, 500.5]
            },
            "index":        [0,    51,   101,   151,   201,   301,   401,   501]
        }

        for i in range(len(table["criteria"][key]) - 1):

            if table["criteria"][key][i] <= concentration < table["criteria"][key][i+1]:

                c_low = table["index"][i]
                c_high = table["index"][i+1] - (1 if isinstance(c_low, int) else 0.1)
                i_low = table["index"][i]
                i_high = table["index"][i+1] - 1

                return round(((i_high - i_low)/(c_high-c_low)) * (concentration - c_low) + i_low, 2)

        return 500
