import csv
import random
import sys

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QGridLayout, QTextEdit, QWizard, QMessageBox, QLineEdit, QWizardPage, QCheckBox, \
    QListView, QSpinBox
from PySide6.QtWidgets import QPushButton, QDialog, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QRegularExpression, Qt
from generate_examples import RandomExample1
from error import ExampleError
from wizard_1_lvl import MyWizard
from list_model import ListModel

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.__result = 0
        self.setWindowTitle("Решение примера с тремя числами")

        layout = QVBoxLayout()

        self.examples = []
        try:
            with open("triple_examples.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.examples.append((row[0], int(row[1])))
        except FileNotFoundError:
            self.examples.append(('-3 - 2 * (-5)', 7))

        self.__example = random.choice(self.examples)
        self.label = QLabel(f'Решите пример: {self.__example[0]}')
        layout.addWidget(self.label)
        self.__spinbox = QSpinBox()
        self.__spinbox.setMinimum(-10000)
        self.__spinbox.setMaximum(10000)
        layout.addWidget(self.__spinbox)

        button = QPushButton("ОК")
        layout.addWidget(button)

        self.setLayout(layout)

        button.clicked.connect(self.close_dialog)

    def reset(self):
        self.__example = random.choice(self.examples)
        self.label.setText(f'Решите пример: {self.__example[0]}')

    @Slot()
    def close_dialog(self):
        if self.__spinbox.value() == self.__example[1]:
            self.__result = 1
        else:
            self.__result = 0
        self.accept()

    def get_result(self):
        return self.__result, self.__example[0]
