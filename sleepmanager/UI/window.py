import sys
from typing import List

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout

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

        self.working_clock.setInterval(1000)
        self.working_clock.timeout.connect(self.update_clock)
        self.working_clock.start()

        main_layout.addWidget(self.timer_label)

        self.apply_styles_to_layout(main_layout, "border: 1px solid black; border-radius: 15px")
        self.timer_label.move(500, 500)

    def update_clock(self):
        self.timer_label.setText(QDateTime.currentDateTime().toString('HH:mm:ss\ndd.MM.yyyy'))

    def apply_styles_to_layout(self, layout, styles):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setStyleSheet(styles)


if __name__ == '__main__':
    app = GUIApp(sys.argv)
    main = MainWindow()
    app.init_widgets([main])

    app.exec()
