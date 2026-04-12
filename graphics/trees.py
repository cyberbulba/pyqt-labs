import csv
import sys
from math import sin, pi, cos

import numpy as np
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QSplineSeries
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QPointF, Qt, QTimer
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

        self.view = gl.GLViewWidget()

        self.layout.addWidget(self.view)

        axis = gl.GLAxisItem()
        axis.setSize(x=100, y=100, z=100)

        self.view.addItem(axis)

        self.view.setCameraPosition(distance=1000, elevation=30, azimuth=45)

        trees_arr_dicts = parse_csv('trees.csv')
        points = get_points(trees_arr_dicts)

        point = gl.GLScatterPlotItem(
            pos=np.array(points),
            size=1,
            color=(1, 0, 0, 1),
            pxMode=False
        )
        self.view.addItem(point)
        QTimer.singleShot(100, self.add_labels)

    def add_labels(self):
        """Добавляем белые подписи осей"""
        labels_config = [
            ("Girth (X)", self.height * 0.8, self.height * 0.9, "yellow"),
            ("Height (Y)", 10, self.height * 0.1, "green"),
            ("Volume (Z)", 10, self.height * 0.9, "blue"),
        ]

        for text, x, y, color in labels_config:
            lbl = QLabel(text, self.view)
            lbl.setStyleSheet(f"color: {color}; font: bold 14px Arial; background: transparent;")
            lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            lbl.move(x, y)
            lbl.show()


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
