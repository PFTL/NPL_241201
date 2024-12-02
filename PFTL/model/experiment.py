import copy

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pathlib
from threading import Thread
from time import sleep
import yaml

from PFTL.model.daq import DAQ
from PFTL.model.dummy_daq import DummyDAQ


class Experiment:
    def __init__(self):
        self.config = {}
        self.copied_config = {}
        self.daq = None
        self.voltages_out = np.empty((1, ))
        self.currents = np.empty((1, ))
        self.scan_running = False
        self.keep_scanning = True
        self.i = 0
        self.last_current = 0

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def initialise(self):
        if self.config['DAQ']['model'] == "Real":
            self.daq = DAQ(self.config['DAQ']['port'])
            self.daq.initialise()
        elif self.config['DAQ']['model'] == "Dummy":
            self.daq = DummyDAQ(self.config['DAQ']['port'])
            self.daq.initialise()

    def start_scan(self):
        if self.scan_running:
            print('Scan already running')
            return

        self.scan_thread = Thread(target=self.scan_voltages)
        self.scan_thread.start()

    def stop_scan(self):
        self.keep_scanning = False

    def scan_voltages(self):
        self.scan_running = True

        self.voltages_out = np.arange(
            self.config['Scan']['start'],
            self.config['Scan']['stop'],
            self.config['Scan']['step'])

        self.copied_config = copy.deepcopy(self.config)

        self.currents = np.zeros_like(self.voltages_out)

        self.i = 0
        self.keep_scanning = True

        for volt in self.voltages_out:
            if not self.keep_scanning:
                break

            self.daq.set_voltage(
                self.config['Scan']['channel_out'],
                volt)

            self.last_current = self.daq.read_voltage(self.config['Scan']['channel_in'])/self.config['DAQ']['resistance']
            self.currents[self.i] = self.last_current
            self.i += 1
        self.scan_running = False

    def save_data(self):
        base_path = pathlib.Path(self.config['Saving']['folder'])
        base_path = base_path / f"{datetime.today():%Y-%m-%d}"

        base_path.mkdir(exist_ok=True, parents=True)

        i = 0
        full_path = base_path / f"{self.config['Saving']['filename']}_{i}.txt"
        while full_path.exists():
            i += 1
            full_path = base_path / f"{self.config['Saving']['filename']}_{i}.txt"

        np.savetxt(full_path, np.stack((self.voltages_out, self.currents)))
        meta_filename = base_path / f"{self.config['Saving']['filename']}_{i}.yml"
        self.save_metadata(full_path=meta_filename)

    def save_metadata(self, full_path):
        with open(full_path, 'w') as f:
            yaml.dump(self.copied_config, f)

    def make_plot(self, ax=None):
        plt.plot(self.voltages_out, self.currents)
        plt.xlabel('Applied Voltage (V)')
        plt.ylabel('Current (A)')
        plt.show()

    def finalise(self):
        self.stop_scan()
        while self.scan_running:
            sleep(0.1)

        self.daq.finalise()


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('Examples/config.yml')
    exp.initialise()
    exp.scan_voltages()
    exp.save_data()
    fig, ax = plt.subplots(1, 2)
    # exp.make_plot()
    exp.config['Scan']['start'] = 2.5
    exp.config['Scan']['step'] = 0.05
    exp.scan_voltages()
    exp.save_data()
    # exp.make_plot()
    exp.finalise()