from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow


app = QApplication([])

win = QMainWindow()
win.show()

directory = QFileDialog.getExistingDirectory(win, 'Select Folder', 
                                    '/Users/aquiles/Documents')
print(directory)

app.exec()



