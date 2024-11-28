from device import SerialDAQ

from time import sleep
import pyvisa
rm = pyvisa.ResourceManager('@py')


class VisaDAQ(SerialDAQ):
    def initialise(self):
        self.dev = rm.open_resource(self.port)
        self.dev.write_termination = '\n'
        self.dev.read_termination = '\r\n'
        sleep(1)

    def query(self, message):
        return self.dev.query(message)


if __name__ == "__main__":
    visa_dev = VisaDAQ('ASRL/dev/cu.usbmodem11201::INSTR')
    visa_dev.initialise()
    print(visa_dev.idn())
    visa_dev.set_output(0, 3.3)
    sleep(1)
    visa_dev.set_output(0, 0)
    visa_dev.finalise()