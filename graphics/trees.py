import csv
import sys
from math import sin, pi, cos

import numpy as np
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QSplineSeries
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QPointF
import pyqtgraph as pg
import pyqtgraph.opengl as gl


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Точечная диаграмма о деревьях")

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

        view = gl.GLViewWidget()
        self.layout.addWidget(view)

        axis = gl.GLAxisItem()
        axis.setSize(x=1000, y=1000, z=1000)
        view.addItem(axis)

        trees_arr_dicts = parse_csv('trees.csv')
        points = get_points(trees_arr_dicts)

        point = gl.GLScatterPlotItem(
            pos=np.array(points),
            size=0.5,
            color=(1, 0, 0, 1),
            pxMode=False
        )
        view.addItem(point)


def parse_csv(csv_file):
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def get_points(trees_arr):
    tree_arr = []
    for tree in trees_arr:
        tree_arr.append([float(tree['Girth']), float(tree['Height']), float(tree['Volume'])])

    return tree_arr


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
