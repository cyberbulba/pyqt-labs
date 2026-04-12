import csv
import sys
from math import sin, pi, cos

import pandas as pd
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QSplineSeries, QValueAxis, QBarCategoryAxis, QBarSet, \
    QBarSeries
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QPointF, Qt
import pyqtgraph as pg


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Столбчатые диаграммы ураганов")

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

        df = pd.read_csv("hurricanes.csv")

        self.create_first_chart(df)
        self.create_second_chart(df)

    def create_first_chart(self, df):
        series = QBarSeries()

        set = QBarSet("")
        set.append(df["2007"].tolist())
        series.append(set)

        chart = QChart()
        chart.legend().setVisible(False)

        chart.addSeries(series)
        chart.setTitle("Столбчатая диаграмма ураганов в 2007 году")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = df["Month"].tolist()
        axis_x = QBarCategoryAxis()
        axis_x.setTitleText("Месяц")
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 50)
        axis_y.setTitleText("Количество ураганов")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        _chart_view = QChartView(chart)
        _chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(_chart_view)

    def create_second_chart(self, df):
        data = []
        for i in range(2005, 2016):
            data.append(int(df[str(i)].sum()))

        series = QBarSeries()

        set = QBarSet("")
        set.append(data)
        series.append(set)

        chart = QChart()
        chart.legend().setVisible(False)

        chart.addSeries(series)
        chart.setTitle("Столбчатая диаграмма ураганов за годы")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = [str(i) for i in range(2005, 2016)]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setTitleText("Год")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 50)
        axis_y.setTitleText("Количество ураганов")
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
