import logging
from BTMUXcontrol import BTMUXcontrol

logging.basicConfig(level=logging.INFO)

class BTSensor(BTMUXcontrol):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def prepare(self, n):
        MUX_pin = n+(n-2)
        BTMUXcontrol().mux_channel(MUX_pin)
        WE = BTMUXcontrol().read_ADC()
        BTMUXcontrol().mux_channel(MUX_pin + 1)
        AE = BTMUXcontrol().read_ADC()
        air_data = [WE,AE]
        return air_data

    def read(self):
        # 0:tmep, 1:pm2.5, 2:co, 3:no2, 4:so2, 5:o3
        if self.id == 0:
            BTMUXcontrol().mux_channel(0)
            mV = BTMUXcontrol().read_ADC()
            v20 = 565
            result = int(mV - v20 + 20)

        elif self.id == 1:
            BTMUXcontrol().mux_channel(1)
            ppdVoltage = BTMUXcontrol().read_ADC() / 1000

            ppd_hppcf = (240.0 * pow (ppdVoltage, 6)) - (2491.3 * pow (ppdVoltage, 5)) + (9448.7 * pow (ppdVoltage, 4)) - (14840.0 * pow (ppdVoltage, 3)) + (10684.0 * pow (ppdVoltage, 2)) + (2211.8 * ppdVoltage) + 7.9623
            calculated_ugm3 = 0.518 + (0.00274 * ppd_hppcf)

            if calculated_ugm3 < 0:
                result = 0
            else:
                result = round(calculated_ugm3,1)

        else:
            result = self.prepare(self.id)

        return result

