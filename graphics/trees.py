import csv
import sys
from math import sin, pi, cos

import pandas as pd
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QSplineSeries, QValueAxis, QBarCategoryAxis, QBarSet, \
    QBarSeries, QScatterSeries
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QPointF, Qt
import pyqtgraph as pg


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Точечные диаграммы о характеристиках деревьев")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.6)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height * 2, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QHBoxLayout(self.central_widget)

        try:
            self.df = pd.read_csv("trees.csv")
        except FileNotFoundError:
            print("Файл не найден, не удастся построить график")
            exit(1)

        self.create_first_chart()
        self.create_second_chart()
        self.create_third_chart()

    def create_first_chart(self):
        series = QScatterSeries()

        for i in range(len(self.df["Girth"].tolist())):
            series.append(self.df["Girth"].tolist()[i], self.df["Height"].tolist()[i])

        chart = QChart()
        chart.legend().setVisible(False)

        chart.addSeries(series)
        chart.setTitle("Зависимость обхвата от высоты дерева")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QValueAxis()
        axis_x.setTitleText("Обхват")
        axis_x.setRange(0, 50)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("Высота")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        _chart_view = QChartView(chart)
        _chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(_chart_view)

    def create_second_chart(self):
        series = QScatterSeries()

        for i in range(len(self.df["Volume"].tolist())):
            series.append(self.df["Volume"].tolist()[i], self.df["Height"].tolist()[i])

        chart = QChart()
        chart.legend().setVisible(False)

        chart.addSeries(series)
        chart.setTitle("Зависимость объёма от высоты дерева")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QValueAxis()
        axis_x.setTitleText("Объём")
        axis_x.setRange(0, 100)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("Высота")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        _chart_view = QChartView(chart)
        _chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(_chart_view)

    def create_third_chart(self):
        series = QScatterSeries()

        for i in range(len(self.df["Girth"].tolist())):
            series.append(self.df["Girth"].tolist()[i], self.df["Volume"].tolist()[i])

        chart = QChart()
        chart.legend().setVisible(False)

        chart.addSeries(series)
        chart.setTitle("Зависимость обхвата от объёма дерева")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QValueAxis()
        axis_x.setTitleText("Обхват")
        axis_x.setRange(0, 50)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("Объём")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        _chart_view = QChartView(chart)
        _chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(_chart_view)


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
