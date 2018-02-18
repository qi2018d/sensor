import threading
import time

from db_manager import DBManager
from neo import Gpio


class SensingThread(threading.Thread):

    selector_pins = [16, 17, 18, 19]
    mux_channel = {
        'no2':{'we':2, 'ae':3},
        'o3':{'we':4, 'ae':5},
        'co':{'we':6, 'ae':7},
        'so2':{'we':8, 'ae':9},
        'temp': 0,
        'pm2_5': 1,
    }
    calibration = {
        'no2' : {
            'n': [1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 1.18, 2.00 ],
            'we_zero': 287,
            'ae_zero': 292,
            'sensitivity': 0.258
        },
        'o3'  : {
            'n' : [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18 ],
            'we_zero': 418,
            'ae_zero': 404,
            'sensitivity': 0.393
        },
        'co'  : {
            'n' : [1.40, 1.03, 0.85, 0.62, 0.30, 0.03, -0.25, -0.48],
            'we_zero': 345,
            'ae_zero': 314,
            'sensitivity': 0.292
        },
        'so2' : {
            'n' : [0.85, 0.85, 0.85, 0.85, 0.85, 1.15, 1.45, 1.75],
            'we_zero' : 333,
            'ae_zero' : 274,
            'sensitivity': 0.288
        }
    }

    read_time = 0.2

    def __init__(self, sender):
        threading.Thread.__init__(self)

        self.sender = sender
        self.gpio = Gpio()

        # init to LOW
        for pin in SensingThread.selector_pins:
            self.gpio.pinMode(pin, self.gpio.OUTPUT)
            self.gpio.digitalWrite(pin, self.gpio.LOW)

    def run(self):
        while True:
            data = self.__read_all()
            print "Raw value : " + str(data)
            DBManager.insert_air_data(data)
            self.sender.send({"type": "real-time", "data": data})

    def __read_all(self):
        """
        Read all sensor values
        :return: json string of sensor values (temp, so2, no2, co, o3, pm25)
        """

        temp = round(self.__read_temp(), 2)
        no2 = round(self.__read_no2_ppb(temp),2)
        o3 = round(self.__read_o3_ppb(temp), 2)
        co = round(self.__read_co_ppm(temp), 2)
        so2 = round(self.__read_so2_ppb(temp), 2)
        pm2_5 = round(self.__read_pm2_5(), 2)
        timestamp = int(time.time())

        return {'temp': temp, 'no2': no2, 'o3':o3, 'co':co, 'so2':so2, 'pm2_5': pm2_5, 'time': timestamp}

    def __read_temp(self):

        channel = SensingThread.mux_channel['temp']
        subtotal = 0.0
        c = 0
        start_time = time.time()

        while time.time() -start_time < SensingThread.read_time:

            mV = self.__read_adc(channel)
            temp = (mV- 500) / 10 - 10

            subtotal += temp
            c += 1

        result = subtotal / c

        if result > 50:
            result = 50
        if result < -20:
            result = -20

        return result
        #return 25
    def __read_no2_ppb(self, temp):
        return self.__calibrate_op('no2', temp)
    def __read_o3_ppb(self, temp):
        return self.__calibrate_op('o3', temp)
    def __read_co_ppm(self, temp):
        return self.__calibrate_op('co', temp) / 1000
    def __read_so2_ppb(self, temp):
        return self.__calibrate_op('so2', temp)
    def __read_pm2_5(self):

        subtotal = 0.0
        c = 0
        start_time = time.time()

        while time.time() -start_time < SensingThread.read_time:

            v = self.__read_adc(SensingThread.mux_channel['pm2_5']) / 1000
            hppcf = 240.0*(v**6) - 2491.3*(v**5) + 9448.7*(v**4) - 14840.0*(v**3) + 10684.0*(v**2) + 2211.8*v + 7.9623
            subtotal += .518 + .00274 * hppcf
            c += 1

        return subtotal / c
    def __calibrate_op(self, name, temp):

        channel_we = SensingThread.mux_channel[name]['we']
        channel_ae = SensingThread.mux_channel[name]['ae']
        calibration = SensingThread.calibration[name]
        zero_we = calibration['we_zero']
        zero_ae = calibration['ae_zero']

        subtotal = 0.0
        c = 0
        start_time = time.time()

        while time.time() -start_time < SensingThread.read_time:

            we = self.__read_adc(channel_we)
            ae = self.__read_adc(channel_ae)

            we = we - zero_we
            ae = ae - zero_ae

            if temp > 50:
                temp = 50
            elif temp < -20:
                temp = -20

            ae = (calibration['n'][int(temp/10) + 2]) * ae
            we = (we - ae) / calibration['sensitivity']

            subtotal += we if we > 0 else 0
            c += 1

        # ppb
        return subtotal / c

    def __read_adc(self, channel):
        s_bin = self.__dec_to_bin(channel)

        # write
        for i in range(4):
            self.gpio.digitalWrite(SensingThread.selector_pins[i], s_bin[i])

        # read
        raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
        scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())

        return raw * scale
    def __dec_to_bin(self, n):
        num = [0, 0, 0, 0]

        if n == 0:
            return num
        else:
            for x in range(n):
                t = x + 1
                for y in range(4):
                    num[y] = t % 2
                    t = t / 2
            return num
