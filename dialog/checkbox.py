import sys

from PySide6.QtWidgets import QPushButton
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

        self.height = int(screen_geometry.height() * 0.3)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.label.setText(f'{self.count}')

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


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
