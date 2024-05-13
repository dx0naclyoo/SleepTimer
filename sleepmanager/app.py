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

        self.working_clock = QtCore.QTimer()
        self.working_clock.setInterval(1000)
        self.working_clock.timeout.connect(self.display_clock)
        self.working_clock.start()

        # Создаем кнопку красного цвета
        self.red_button = Qtw.QPushButton('Delete')
        self.red_button.setStyleSheet('''
            QPushButton {
                background-color: #FF6666;
                border: 2px solid #FF3333;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
            }

            QPushButton:pressed {
                background-color: #FF3333;
                border: 2px solid #FF0000;
            }
        ''')
        self.red_button.setFixedSize(150, 50)
        self.red_button.clicked.connect(self.button_clicked)

        # Создаем кнопку зеленого цвета
        self.green_button = Qtw.QPushButton('Add Shutdown')
        self.green_button.setStyleSheet('''
        QPushButton {
            background-color: #00FF00;
            border: 2px solid #00CC00;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
        }

        QPushButton:pressed {
            background-color: #00CC00;
            border: 2px solid #009900;
        }
        ''')
        self.green_button.setFixedSize(150, 50)
        self.green_button.clicked.connect(self.button_clicked)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.green_button)
        self.layout().addWidget(self.red_button)
        self.show()

    def display_clock(self):
        self.label.setText(QDateTime.currentDateTime().toString('HH:mm:ss\ndd MM yyyy'))

    def button_clicked(self):
        # Определяем функцию, которая будет вызываться при нажатии на кнопку
        sender_button = app.focusWidget()
        if sender_button is self.red_button:
            print("Нажата красная кнопка")
        elif sender_button is self.green_button:
            self.add_shutdown()
            print("Нажата зеленая кнопка")

    def add_shutdown(self):
        time, ok_pressed = Qtw.QInputDialog.getInt(self, "Enter Time", "Enter time in seconds:")
        print(ok_pressed)
        if ok_pressed:
            hours = time // 3600
            minutes = (time % 3600) // 60
            seconds = time % 60
            print(f"Shutdown set for: {hours} hours, {minutes} minutes, {seconds} seconds")


if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    window = Window()
    app.exec()
