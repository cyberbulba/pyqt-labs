import sys

from PyQt6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout


class MyWindow(QMainWindow):
    def __init__(self, height, screen_geometry):
        super().__init__()

        self.resize(height, height)

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

    label = QLabel()
    layout.addWidget(label)
    label.setWordWrap(True)
    label.setText("bear" * 100)

    label.resize(height, 200)

    font = QFont("Times New Roman", 14)
    font.setItalic(True)

    label.setFont(font)

    window.show()
    label.show()
    app.exec()


if __name__ == "__main__":
    main()
