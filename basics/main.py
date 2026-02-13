import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class MyWindow(QWidget):
    def __init__(self, height, screen_geometry):
        super().__init__()

        self.setFixedSize(height, height)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


def main():
    app = QApplication(sys.argv)

    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    height = screen_geometry.height()

    window = MyWindow(height, screen_geometry)
    layout = QVBoxLayout(window)


    label1 = QLabel()
    label1.setWordWrap(True)
    label1.setText("bear " * 120)
    label1.resize(height, 20)
    font = QFont("Times New Roman", 14)
    font.setItalic(True)
    label1.setFont(font)
    label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label1.setMargin(15)
    layout.addWidget(label1)


    label2 = QLabel("Hello World")
    font = QFont("Times New Roman", 28)
    label2.setFont(font)
    label2.setMargin(15)
    label2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
    layout.addWidget(label2)


    label3 = QLabel()
    pixmap = QPixmap("boloto.jpg")
    label3.setPixmap(pixmap)
    layout.addWidget(label3)


    window.show()
    app.exec()


if __name__ == "__main__":
    main()
