import sys

from PySide6.QtCore import Slot, QLineF, QPointF, QRectF
from PySide6.QtGui import QPainter, QPolygonF, QPen, Qt, QBrush, QColor, QGradient, QLinearGradient
from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Фигуры")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.3)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height * 2, self.height * 2)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

    def paintEvent(self, event):
        pen_1 = QPen()
        pen_1.setStyle(Qt.DashDotLine)
        pen_1.setWidth(3)
        pen_1.setBrush(Qt.red)
        brush_1 = QBrush(QColor(0, 255, 0))

        painter = QPainter(self)
        painter.setPen(pen_1)
        painter.setBrush(brush_1)
        points = QPolygonF([QPointF(self.height // 4, 0),
                            QPointF(0, self.height // 2),
                            QPointF(self.height // 2, self.height // 2)
                            ])
        painter.drawPolygon(points)

        painter.drawRect(QRectF(0, 10 + self.height // 2, self.height // 2, self.height // 2))

        gradient = QLinearGradient(0, 1, 1, 0)
        gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, Qt.yellow)
        gradient.setColorAt(0.5, Qt.blue)
        gradient.setColorAt(1.0, Qt.green)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QRectF(self.height // 2, 0, self.height, self.height // 2))


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
