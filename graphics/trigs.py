import sys
from math import sin, pi, cos

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QSplineSeries
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QPointF
import pyqtgraph as pg


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Графики тригонометрии")

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
        self.layout.addWidget(QLabel("График синуса"))

        self.chart_1 = QChart()
        self.chart_1.legend().hide()

        self.series_1 = QSplineSeries()
        self.create_series_1()

        self.chart_1.addSeries(self.series_1)
        self.chart_1.createDefaultAxes()

        self.chart_view_1 = QChartView(self.chart_1)
        self.layout.addWidget(self.chart_view_1)

        self.layout.addWidget(QLabel("График косинуса"))

        self.chart_2 = QChart()
        self.chart_2.legend().hide()

        self.series_2 = QSplineSeries()
        self.create_series_2()

        self.chart_2.addSeries(self.series_2)
        self.chart_2.createDefaultAxes()

        self.chart_view_2 = QChartView(self.chart_2)
        self.layout.addWidget(self.chart_view_2)

    def create_series_1(self):
        x = -5
        for i in range(100):
            self.series_1.append(QPointF(x, sin(x)))
            x += 0.1

    def create_series_2(self):
        x = -5
        for i in range(100):
            self.series_2.append(QPointF(x, cos(x)))
            x += 0.1



def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
