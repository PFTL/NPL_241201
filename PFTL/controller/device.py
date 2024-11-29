from serial import Serial
from time import sleep
import numpy as np


class SerialDAQ:
    def __init__(self, port):
        self.port = port
        self.dev = None  # This gets a value in initialise 

    def initialise(self):
        self.dev = Serial(self.port)
        sleep(1)

    def query(self, message):
        out = message + '\n'
        
        if self.dev is None:
            raise Exception('Device is not initialized')

        self.dev.write(out.encode('ascii'))

        ans = self.dev.readline()
        ans = ans.decode().strip()
        if ans.startswith('ERROR'):
            raise Exception(f'Command: {out} returned an Error: {ans}')
        return ans

    def idn(self):
        return self.query('*IDN?')

    def set_output(self, channel_out, value):
        if value > 4095:
            raise Exception(f'Value {value} outside range 0-4095')
        
        out = f'OUT:CH{channel_out} {value}'
        self.query(out)

    def get_input(self, channel_in):
        out = f'MEAS:CH{channel_in}?'
        return int(self.query(out))

    def finalise(self):
        self.dev.close()


if __name__ == '__main__':
    serial_dev = SerialDAQ('/dev/cu.usbmodem11201', 220)
    serial_dev.initialise()
    idn = serial_dev.idn()
    print(f'Serial Device with IDN: {idn}')
    print(serial_dev)

    currents = []

    start = 3.0
    stop = 3.6
    step = 0.01

    voltages = np.arange(start, stop, step)

    try:
        for volt in voltages:
            serial_dev.set_output(0, volt)
            current = serial_dev.get_input(0)
            currents.append(current)
            print(volt, current)
    except Exception as e:
        raise e
    finally:
        serial_dev.finalise()

    print(voltages, currents)