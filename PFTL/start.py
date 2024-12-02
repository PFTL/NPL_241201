from PFTL.model.experiment import Experiment
from PFTL.view.main_window import ScanWindow

from PyQt5.QtWidgets import QApplication

def main():
    exp = Experiment()
    exp.load_config('Examples/config.yml')
    exp.initialise()

    app = QApplication([])
    win = ScanWindow(exp)
    win.show()
    app.exec()

    exp.finalise()


if __name__ == "__main__":
    main()