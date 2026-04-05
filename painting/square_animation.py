import sys

from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import Slot, QLineF, QPointF, QRectF, QParallelAnimationGroup, QPoint, QEasingCurve
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
        self.setWindowTitle("Анимация")

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
        self.square_widget = SquareWidget(self.height)
        self.label = QLabel("Виджет 2")
        self.layout.addWidget(self.square_widget)
        self.layout.addWidget(self.label)

        anim_1 = QPropertyAnimation(self.square_widget, b"pos", self)

        anim_1.setDuration(5000)
        anim_1.setKeyValueAt(0.0, QPoint(0, 0))
        anim_1.setKeyValueAt(0.2, QPoint(self.height // 4, self.height // 2))
        anim_1.setKeyValueAt(0.4, QPoint(self.height // 4, 0))
        anim_1.setKeyValueAt(0.6, QPoint(self.height // 2, self.height // 2))
        anim_1.setKeyValueAt(0.8, QPoint(self.height // 2, 0))
        anim_1.setEndValue(QPoint(self.height // 2, self.height // 4))
        anim_1.setEasingCurve(QEasingCurve.Linear)

        anim_2 = QPropertyAnimation(self.label, b"pos", self)

        anim_2.setDuration(5000)
        anim_2.setKeyValueAt(0.0, QPoint(self.height // 2, 0))
        anim_2.setKeyValueAt(0.2, QPoint(self.height // 4, self.height // 2))
        anim_2.setKeyValueAt(0.4, QPoint(0, self.height // 4))
        anim_2.setKeyValueAt(0.6, QPoint(self.height // 2, self.height // 2))
        anim_2.setKeyValueAt(0.8, QPoint(0, self.height // 2))
        anim_2.setEndValue(QPoint(self.height // 2, self.height // 4))
        anim_2.setEasingCurve(QEasingCurve.Linear)

        animation = QParallelAnimationGroup(self)
        animation.addAnimation(anim_1)
        animation.addAnimation(anim_2)
        animation.start()


def main():
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
