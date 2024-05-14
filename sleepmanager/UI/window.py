import sys
from typing import List

from sleepmanager.SleepService.service import SleepService, SleepServiceWindows

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

    def __init__(self, sleep_service, parent=None, ):
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
            return

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
    def __init__(self, sleep_service: SleepService):
        super().__init__()
        self.sleep_service = sleep_service
        self.timer_label = QLabel()
        self.working_clock = QtCore.QTimer()
        self.shutdown_label_clock = QtCore.QTimer()
        self.delete_button = QPushButton()
        self.add_button = QPushButton()
        self.dialog = AddDateDialog(self)
        self.shutdowns: int = 0
        self.new_shutdown_label = None

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

        self.shutdown_label_clock.timeout.connect(self.update_shutdown_label_clock)

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

        self.top_layout = QVBoxLayout()  # Создание нового вертикального макета для верхней области
        shutdown_list_label = QLabel("Тут будет ваш таймер сна :)")  # Добавление элементов в верхний макет
        self.top_layout.addWidget(shutdown_list_label)
        shutdown_list_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 18px;
                padding: 10px;
                border-radius: 5px;
                background-color: #f0f0f0;
                transition: background-color 0.3s;
            }

        """)

        buttons_layout = QHBoxLayout()  # Создание нового горизонтального макета для кнопок
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)

        combined_layout = QVBoxLayout()
        combined_layout.addLayout(self.top_layout)
        combined_layout.addLayout(buttons_layout)

        main_layout.addWidget(self.timer_label)
        main_layout.addLayout(combined_layout)

        self.top_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)  # Установка координат и размера

    def update_clock(self):
        self.timer_label.setText(QDateTime.currentDateTime().toString('HH:mm:ss\ndd.MM.yyyy'))

    def button_click(self, button):
        if button == "add":
            print("Нажата кнопка: add")
            self.add_shutdown_label()
        else:
            print("Нажата кнопка: delete")
            if self.new_shutdown_label:
                self.delete_shutdown_label()

    def handler_seconds_input(self, seconds):
        if seconds:
            self.shutdowns = seconds

            print("handler", seconds)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            remaining_seconds = seconds % 60

            result = f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
            if self.new_shutdown_label is None:  # Если метка не создана, создаем её
                self.new_shutdown_label = QLabel(f"shutdown, {result}", self)
                self.top_layout.addWidget(self.new_shutdown_label)
                self.new_shutdown_label.setStyleSheet("""
                    QLabel {
                        color: #333;
                        font-size: 15px;
                        padding: 5px;
                        border-radius: 15px;
                        border: 1px solid black; /* добавляем границу */
                        background-color: #f0f0f0;
                        transition: background-color 0.3s, box-shadow 0.3s; /* добавляем тень в анимацию */
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* добавляем тень */
                    }
                    QLabel:hover {
                        background-color: #ddd;
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.5); /* увеличиваем тень при наведении */
                    }
                """)
                self.new_shutdown_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
                if self.shutdowns > 0:
                    self.shutdown_label_clock.start(1000)
            else:
                # Если метка уже существует, просто обновляем её текст
                self.new_shutdown_label.setText(f"shutdown, {result}")
                if self.shutdowns > 0:
                    self.shutdown_label_clock.start(1000)

    def update_shutdown_label_clock(self):
        if self.shutdowns > 0:
            self.shutdowns -= 1
            hours = self.shutdowns // 3600
            minutes = (self.shutdowns % 3600) // 60
            remaining_seconds = self.shutdowns % 60
            result = f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
            self.new_shutdown_label.setText(f"shutdown, {result}")
        else:
            if self.new_shutdown_label:
                self.delete_shutdown_label()

    def add_shutdown_label(self):
        self.dialog.show()
        self.dialog.dataEntered.connect(self.handler_seconds_input)
        self.dialog.exec()
        self.dialog.dataEntered.disconnect()
        self.sleep_service.fake_shutdown(self.shutdowns)

    def delete_shutdown_label(self):
        self.shutdown_label_clock.stop()
        self.top_layout.removeWidget(self.new_shutdown_label)
        self.new_shutdown_label.deleteLater()
        self.new_shutdown_label = None
        self.sleep_service.cancel_shutdown()


if __name__ == '__main__':
    app = GUIApp(sys.argv)
    main = MainWindow(SleepServiceWindows())

    app.init_widgets([main])

    app.exec()
