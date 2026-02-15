import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.height = screen_geometry.height()

        self.setFixedSize(self.height, self.height)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())
        self.create_text_label_1()
        self.create_text_label_2()
        self.create_image_label()

    def create_text_label_1(self):
        label1 = QLabel(self)
        label1.setWordWrap(True)
        label1.setText("hello world! " * 100)
        label1.resize(self.height, self.height // 3)
        font = QFont("Times New Roman", 14)
        font.setItalic(True)
        label1.setFont(font)
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setMargin(15)

    def create_text_label_2(self):
        label2 = QLabel(self)
        label2.setText("Hello World")
        font = QFont("Times New Roman", 28)
        label2.resize(self.height, self.height // 3)
        label2.setFont(font)
        label2.setMargin(15)
        label2.move(0, self.height // 3)
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

    def create_image_label(self):
        label3 = QLabel(self)
        pixmap = QPixmap("boloto.jpg")
        pixmap = pixmap.scaledToHeight(self.height // 3)
        label3.setPixmap(pixmap)
        label3.move(0, 2 * self.height // 3)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
