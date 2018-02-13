import threading
from neo import Gpio

class BTMUXcontrol:
    def __init__(self):
        self.temp = 0
        self.output_pins = [24, 25, 26, 27]
        self.IOLock = threading.Lock()  # mutual lock for R/W control
        self.gpio = Gpio()              # initialize GPIO controller

        # setup output pins
        self.IOLock.acquire()
        for pin in self.output_pins:
            self.gpio.pinMode(pin, self.gpio.OUTPUT)
            self.gpio.digitalWrite(pin, self.gpio.LOW)
        self.IOLock.release()

    def decToBin(self, n):
        num = [0,0,0,0]
        if n == 0:
            return num
        else:
            for x in range(n):
                t = x + 1
                for y in range(4):
                    num[y] = t%2
                    t = t/2
            return num

    def mux_channel(self, channel):
        bin_list = self.decToBin(channel) #binary list
        self.IOLock.acquire()
        for z in range(4):
            self.gpio.digitalWrite(self.output_pins[z],bin_list[z])
        self.IOLock.release()
        #return True

    def read_ADC(self):
        self.IOLock.acquire()
        raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
        scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
        vout = raw * scale
        self.IOLock.release()
        return vout

