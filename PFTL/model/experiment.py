import matplotlib.pyplot as plt
import numpy as np
import pathlib
from threading import Thread
import yaml

from PFTL.model.daq import DAQ


class Experiment:
    def __init__(self):
        self.config = {}
        self.daq = None
        self.voltages_out = np.empty((1, ))
        self.currents = np.empty((1, ))

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def initialise(self):
        self.daq = DAQ(self.config['DAQ']['port'])
        self.daq.initialise()

    def start_scan(self):
        self.scan_thread = Thread(target=self.scan_voltages)
        self.scan_thread.start()

    def scan_voltages(self):
        self.voltages_out = np.arange(
            self.config['Scan']['start'],
            self.config['Scan']['stop'],
            self.config['Scan']['step'])

        self.currents = np.zeros_like(self.voltages_out)

        i = 0 
        for volt in self.voltages_out:
            self.daq.set_voltage(
                self.config['Scan']['channel_out'],
                volt)
            
            self.currents[i] = self.daq.read_voltage(self.config['Scan']['channel_in'])/self.config['DAQ']['resistance']
            i += 1
            
    def save_data(self):
        base_path = pathlib.Path(self.config['Saving']['folder'])
        base_path.mkdir(exist_ok=True, parents=True)

        full_path = base_path / self.config['Saving']['filename'] 

        np.savetxt(full_path, np.stack((self.voltages_out, self.currents)))
        self.save_metadata()

    def save_metadata(self):
        base_path = pathlib.Path(self.config['Saving']['folder'])
        base_path.mkdir(exist_ok=True, parents=True)

        full_path = base_path / (self.config['Saving']['filename'] + ".yml")
        with open(full_path, 'w') as f:
            yaml.dump(self.config, f)

    def make_plot(self):
        plt.plot(self.voltages_out, self.currents)
        plt.xlabel('Applied Voltage (V)')
        plt.ylabel('Current (A)')
        plt.show()

    def finalise(self):
        self.daq.finalise()


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('Examples/config.yml')
    exp.initialise()
    exp.scan_voltages()
    exp.save_data()
    # exp.make_plot()
    exp.config['Scan']['start'] = 2.5
    exp.config['Scan']['step'] = 0.05
    exp.scan_voltages()
    exp.save_data()
    # exp.make_plot()
    exp.finalise()