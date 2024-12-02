from PFTL.controller.device import SerialDAQ
from time import sleep


class DAQ:
    def __init__(self, device_num):
        self.device_num = device_num
        self.driver = None

    def initialise(self):
        port = f'COM{self.device_num}'
        port = f'/dev/cu.usbmodem{self.device_num}'  # Only for Mac
        self.driver = SerialDAQ(port)
        self.driver.initialise()

    def finalise(self):
        self.set_voltage(0, 0)
        self.set_voltage(1, 0)
        self.driver.finalise()

    def set_voltage(self, channel, volts):
        volts_int = int(volts * 4095 / 3.3)
        self.driver.set_output(channel, volts_int)

    def read_voltage(self, channel):
        """Returns the value in volts"""
        
        volts_int = self.driver.get_input(channel)
        return volts_int * 3.3 / 1023

    def check(self):
        for _ in range(5):
            self.set_voltage(0, 3.3)
            self.set_voltage(1, 3.3)
            sleep(0.5)
            self.set_voltage(0, 0)
            self.set_voltage(1, 0)
            sleep(0.5)

    def __str__(self):
        serial_number = self.driver.idn()
        return f"DAQ {serial_number} on {self.device_num}"


if __name__ == "__main__":
    dev = DAQ(11201)
    dev.initialise()
    print(dev)
    dev.check()