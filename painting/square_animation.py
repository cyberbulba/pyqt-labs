import sys

from PySide6.QtCore import Slot, QLineF, QPointF, QRectF
from PySide6.QtGui import QPainter, QPolygonF, QPen, Qt, QBrush, QColor, QGradient, QLinearGradient
from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout


class SquareWidget(QWidget):
    def __init__(self, height):
        super().__init__()
        self.height = height

    def paintEvent(self, event):
        pen = QPen()
        pen.setWidth(3)
        pen.setBrush(Qt.green)
        brush = QBrush(QColor(0, 255, 0))

        painter = QPainter(self)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(QRectF(0, 0, self.height // 4, self.height // 4))


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Квадрат")

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
        self.layout.addWidget(SquareWidget(self.height))


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
