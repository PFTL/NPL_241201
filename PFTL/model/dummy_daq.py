import numpy as np
from time import sleep


class DummyDAQ:
    def __init__(self, device_num):
        self.device_num = device_num

    def initialise(self):
        sleep(1)
        print('Device initialized')

    def finalise(self):
        print('Device Finalised')

    def set_voltage(self, channel, volts):
        return

    def read_voltage(self, channel):
        sleep(0.01)
        return np.random.random()

    def check(self):
        pass

    def __str__(self):
        return f"Dummy DAQ {self.device_num}"