import sys

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Счётчик")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.2)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.create_text_label_1()  # создаём метки

        button1 = QPushButton("Увеличить число")
        self.layout.addWidget(button1)
        button1.clicked.connect(self.count_up)

        button2 = QPushButton("Обнулить счётчик")
        self.layout.addWidget(button2)
        button2.clicked.connect(self.count_clear)

    @Slot()
    def count_up(self):
        self.count += 1
        self.label.setText(f"{self.count}")

    @Slot()
    def count_clear(self):
        self.count = 0
        self.label.setText(f"{self.count}")

    def create_text_label_1(self):
        self.label = QLabel()
        self.label.setWordWrap(True)  # перенос слов в label'е
        self.label.resize(self.height, self.height // 3)
        font = QFont("Times New Roman", 14)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        self.label.setMargin(15)
        self.layout.addWidget(self.label)
        self.label.setText(f'{self.count}')


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
