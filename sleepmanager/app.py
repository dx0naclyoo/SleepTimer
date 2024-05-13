import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton


class SleepManager(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Создаем виджеты
        self.label = QLabel('Привет, мир!')
        self.button = QPushButton('Нажми меня')





if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем экземпляр виджета
    widget = SleepManager()
    widget.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec())
