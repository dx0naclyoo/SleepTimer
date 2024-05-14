import sys
from typing import List

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QDateTime, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QDialog, QVBoxLayout, \
    QLineEdit

UI_BASE_DIR = sys.path[0]


class GUIApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

    @staticmethod
    def init_widgets(list_widgets: List[QWidget]):
        for in_widget in list_widgets:
            in_widget.show()


class AddDateDialog(QDialog):
    dataEntered = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите секунды")

        layout = QVBoxLayout()

        self.seconds_label = QLabel("Секунды:")
        self.seconds_input = QLineEdit()

        self.result_label = QLabel()

        self.dialog_add_button = QPushButton("Добавить")
        self.dialog_add_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; "
                                             "border: 1px solid #357035; "
                                             "border-radius: 5px; min-width: 50px; min-height: 30px; }"
                                             "QPushButton:hover { background-color: #45a049; }"
                                             "QPushButton:pressed { background-color: #357035; }")

        self.seconds_input.textChanged.connect(self.calculate_time)
        self.dialog_add_button.clicked.connect(lambda: self.send_data(self.seconds_input.text()))

        layout.addWidget(self.seconds_label)
        layout.addWidget(self.seconds_input)
        layout.addWidget(self.result_label)
        layout.addWidget(self.dialog_add_button)

        self.setLayout(layout)

    def send_data(self, sec_inp):
        if sec_inp.isdigit():
            seconds = int(sec_inp)
            self.dataEntered.emit(seconds)
            self.accept()

        self.seconds_input.clear()

    def calculate_time(self):
        try:
            seconds = int(self.seconds_input.text())
            if seconds < 0:
                raise ValueError("Отрицательное значение")

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            remaining_seconds = seconds % 60

            self.result_label.setText(f"{hours} часов {minutes} минут {remaining_seconds} секунд")
        except ValueError as e:
            self.result_label.setText("Ошибка: " + str(e))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.timer_label = QLabel()
        self.working_clock = QtCore.QTimer()
        self.delete_button = QPushButton()
        self.add_button = QPushButton()
        self.dialog = AddDateDialog(self)
        self.shutdowns: int = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('SleepManager')
        self.setGeometry(350, 250, 500, 250)
        self.setWindowIcon(QtGui.QIcon(f"{UI_BASE_DIR}/sleep.png"))

        main_layout = QHBoxLayout(self)

        self.dialog.setGeometry(500, 350, 200, 50)

        self.timer_label = QLabel(QtCore.QDateTime.currentDateTime().toString('HH:mm:ss\ndd.MM.yyyy'))
        self.timer_label.setStyleSheet("QLabel "
                                       "{ "
                                       "color: white; "
                                       "font-size: 24px; "
                                       "padding: 10px 25px 10px 25px; "
                                       "background-color: #333; "
                                       "text-align: center; "
                                       "border-radius: 10px; }")

        self.working_clock.setInterval(1000)
        self.working_clock.timeout.connect(self.update_clock)
        self.working_clock.start()

        self.add_button = QPushButton()
        self.add_button.setText('Add Shutdown')
        self.add_button.setFixedSize(100, 30)
        self.add_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; "
                                      "border: 1px solid #357035; "
                                      "border-radius: 5px; min-width: 140px; min-height: 30px; }"
                                      "QPushButton:hover { background-color: #45a049; }"
                                      "QPushButton:pressed { background-color: #357035; }")
        self.add_button.clicked.connect(lambda: self.button_click("add"))

        self.delete_button = QPushButton()
        self.delete_button.setText('Delete')
        self.delete_button.setFixedSize(100, 30)
        self.delete_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; "
                                         "border: 1px solid #801515; "
                                         "border-radius: 5px; min-width: 140px; min-height: 30px; }"
                                         "QPushButton:hover { background-color: #d32f2f; }"
                                         "QPushButton:pressed { background-color: #801515; }")
        self.delete_button.clicked.connect(lambda: self.button_click("delete"))

        buttons_layout = QHBoxLayout()  # Создание нового горизонтального макета для кнопок
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)

        main_layout.addWidget(self.timer_label)
        main_layout.addStretch(200)
        main_layout.addLayout(buttons_layout)

        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)  # Установка координат и размера

    def update_clock(self):
        self.timer_label.setText(QDateTime.currentDateTime().toString('HH:mm:ss\ndd.MM.yyyy'))

    def button_click(self, button):
        if button == "add":
            print("Нажата кнопка: add")
            self.dialog.show()
            self.dialog.dataEntered.connect(self.handler_seconds_input)
            self.dialog.exec()

        else:
            print("Нажата кнопка: delete")

    def handler_seconds_input(self, seconds):
        print("Seconds:", seconds)

if __name__ == '__main__':
    app = GUIApp(sys.argv)
    main = MainWindow()
    app.init_widgets([main])

    app.exec()
