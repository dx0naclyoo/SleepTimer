import sys

from PyQt6.QtCore import QDateTime

from sleepmanager.SleepService.service import ShutdownService

import PyQt6.QtWidgets as Qtw
from PyQt6 import QtGui, QtCore


class Window(Qtw.QWidget):
    def __init__(self):
        super().__init__()

        # add a title
        self.setWindowTitle("Sleep Manager")
        # set icon
        self.setWindowIcon(QtGui.QIcon("UI/sleep.png"))
        # set size and position
        self.setGeometry(400, 250, 500, 250)
        # set layout
        self.setLayout(Qtw.QVBoxLayout())

        # Create a Label
        self.label = Qtw.QLabel(QDateTime.currentDateTime().toString('HH:mm:ss\ndd MM yyyy'))
        self.layout().addWidget(self.label)

        self.working_clock = QtCore.QTimer()
        self.working_clock.setInterval(1000)
        self.working_clock.timeout.connect(self.display_clock)
        self.working_clock.start()

        self.show()

    def display_clock(self):
        self.label.setText(QDateTime.currentDateTime().toString('HH:mm:ss\ndd MM yyyy'))


if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    window = Window()
    app.exec()
