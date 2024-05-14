import sys
from typing import List

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QPushButton

UI_BASE_DIR = sys.path[0]


class GUIApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)

    @staticmethod
    def init_widgets(list_widgets: List[QWidget]):
        for in_widget in list_widgets:
            in_widget.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.timer_label = QLabel()
        self.working_clock = QtCore.QTimer()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('SleepManager')
        self.setGeometry(350, 250, 500, 250)
        self.setWindowIcon(QtGui.QIcon(f"{UI_BASE_DIR}/sleep.png"))

        main_layout = QHBoxLayout(self)

        self.timer_label = QLabel(QtCore.QDateTime.currentDateTime().toString('HH:mm:ss\ndd.MM.yyyy'))
        self.timer_label.setStyleSheet("QLabel "
                                       "{ "
                                       "color: white; "
                                       "font-size: 24px; "
                                       "padding: 10px 40px 10px 40px; "
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
                                      "border-radius: 5px; min-width: 120px; min-height: 30px; }"
                                      "QPushButton:hover { background-color: #45a049; }"
                                      "QPushButton:pressed { background-color: #357035; }")

        self.delete_button = QPushButton()
        self.delete_button.setText('Delete')
        self.delete_button.setFixedSize(100, 30)
        self.delete_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; "
                                         "border: 1px solid #801515; "
                                         "border-radius: 5px; min-width: 120px; min-height: 30px; }"
                                         "QPushButton:hover { background-color: #d32f2f; }"
                                         "QPushButton:pressed { background-color: #801515; }")

        buttons_layout = QHBoxLayout()  # Создание нового горизонтального макета для кнопок
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)

        main_layout.addWidget(self.timer_label)
        main_layout.addStretch(200)
        main_layout.addLayout(buttons_layout)

        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)  # Установка координат и размера

    def update_clock(self):
        self.timer_label.setText(QDateTime.currentDateTime().toString('HH:mm:ss\ndd.MM.yyyy'))


if __name__ == '__main__':
    app = GUIApp(sys.argv)
    main = MainWindow()
    app.init_widgets([main])

    app.exec()
