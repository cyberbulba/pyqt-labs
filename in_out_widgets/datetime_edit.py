import sys

import datetime as dt
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDateTimeEdit
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Рассчёт возраста:")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.6)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        self.layout.addWidget(label)
        label.setText("Выберите дату:")

        self.dateTimeEdit = QDateTimeEdit(QDate.currentDate())

        self.dateTimeEdit.setDisplayFormat("yyyy.MM.dd")
        self.dateTimeEdit.setCalendarPopup(True)
        self.layout.addWidget(self.dateTimeEdit)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.dateTimeEdit.dateTimeChanged.connect(self.handle_date)

    @Slot()
    def handle_date(self):
        birth_date = self.dateTimeEdit.date()
        birth_date_dt = dt.datetime(birth_date.year(), birth_date.month(), birth_date.day())

        if not birth_date_dt >= dt.datetime.now():
            delta = dt.datetime.now() - birth_date_dt

            s = round(delta.total_seconds())
            hours = round(s // 3600)
            years = round(s // (3600 * 24 * 365))

            self.text_edit.setText(f'Вы живёте полных лет: {years} \nили {hours} часов \nили {s} секунд')
        else:
            self.text_edit.setText('Вы ввели неправильную дату!')


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
