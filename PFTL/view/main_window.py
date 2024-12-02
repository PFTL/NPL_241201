import pathlib
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic

from PFTL.model.experiment import Experiment


view_folder = pathlib.Path(__file__).parent


class ScanWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment

        uic.loadUi(str(view_folder/'main_window.ui'), self)

        self.start_button.clicked.connect(self.start_pressed)
        self.stop_button.clicked.connect(self.experiment.stop_scan)
        self.plot_button.clicked.connect(self.experiment.make_plot)

        self.actionSave.triggered.connect(self.experiment.save_data)

        self.start_line.setText(str(self.experiment.config['Scan']['start']))
        self.stop_line.setText(str(self.experiment.config['Scan']['stop']))
        self.step_line.setText(str(self.experiment.config['Scan']['step']))

        self.plot = self.plot_widget.plot([0, ], [0, ])
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.start(100)

    def start_pressed(self):
        print('Start Pressed')
        self.experiment.config['Scan'].update({
            'start': float(self.start_line.text()),
            'stop': float(self.stop_line.text()),
            'step': float(self.step_line.text()),
        })
        self.experiment.start_scan()
        self.plot.setData(self.experiment.voltages_out, self.experiment.currents)

    def update_plot(self):
        self.plot.setData(self.experiment.voltages_out, self.experiment.currents)

if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('Examples/config.yml')
    exp.initialise()

    app = QApplication([])
    win = ScanWindow(exp)
    win.show()
    app.exec()

    exp.finalise()