import sys

from PySide6.QtWidgets import QPushButton, QSpinBox, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0

        self.first_number = None
        self.second_number = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Калькулятор")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.5)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.line_edit1 = QLineEdit()
        self.layout.addWidget(self.line_edit1)
        self.create_text_label("Введите первое число")

        self.line_edit2 = QLineEdit()
        self.layout.addWidget(self.line_edit2)
        self.create_text_label("Введите второе число")

        button1 = QPushButton("+")
        self.layout.addWidget(button1)
        button1.clicked.connect(self.plus)

        button1 = QPushButton("-")
        self.layout.addWidget(button1)
        button1.clicked.connect(self.minus)

        button1 = QPushButton("*")
        self.layout.addWidget(button1)
        button1.clicked.connect(self.mult)

        button1 = QPushButton("/")
        self.layout.addWidget(button1)
        button1.clicked.connect(self.division)

        button1 = QPushButton("=")
        self.layout.addWidget(button1)
        button1.clicked.connect(self.count_up)

        self.create_text_label("Результат:")

        self.rez_label = QLabel()
        self.layout.addWidget(self.rez_label)

    @Slot()
    def count_up(self):
        self.count += 1
        self.label.setText(f"{self.count}")

    @Slot()
    def count_clear(self):
        self.count = 0
        self.label.setText(f"{self.count}")

    @Slot()
    def plus(self):
        self.rez_label.setText("")

        text1 = self.line_edit1.text()
        text2 = self.line_edit2.text()

        if text1.isdigit() and text2.isdigit():
            self.rez_label.setText(f"{text1} + {text2} = {int(text1) + int(text2)}")
        else:
            self.rez_label.setText("Введены неправильные числа!")

    @Slot()
    def minus(self):
        self.rez_label.setText("")

        text1 = self.line_edit1.text()
        text2 = self.line_edit2.text()

        if text1.isdigit() and text2.isdigit():
            self.rez_label.setText(f"{text1} - {text2} = {int(text1) - int(text2)}")
        else:
            self.rez_label.setText("Введены неправильные числа!")

    @Slot()
    def mult(self):
        self.rez_label.setText("")

        text1 = self.line_edit1.text()
        text2 = self.line_edit2.text()

        if text1.isdigit() and text2.isdigit():
            self.rez_label.setText(f"{text1} * {text2} = {int(text1) * int(text2)}")
        else:
            self.rez_label.setText("Введены неправильные числа!")

    @Slot()
    def division(self):
        self.rez_label.setText("")

        text1 = self.line_edit1.text()
        text2 = self.line_edit2.text()

        if text1.isdigit() and text2.isdigit():
            self.rez_label.setText(f"{text1} // {text2} = {int(text1) / int(text2)}")
        else:
            self.rez_label.setText("Введены неправильные числа!")

    def create_text_label(self, text):
        self.label = QLabel()
        self.label.setWordWrap(True)  # перенос слов в label'е
        font = QFont("Times New Roman", 14)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        self.label.setMargin(15)
        self.layout.addWidget(self.label)
        self.label.setText(text)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
