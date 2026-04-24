import random
import sys

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QGridLayout, QTextEdit, QWizard, QMessageBox, QLineEdit, QWizardPage, QCheckBox
from PySide6.QtWidgets import QPushButton, QDialog, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QRegularExpression, Qt
from generate_examples import RandomExample1


class ExamplePage(QWizardPage):
    def __init__(self, action=None, sign=1):
        super().__init__()
        label = QLabel("Решите пример:")

        layout = QVBoxLayout(self)
        layout.addWidget(label)

        if action is None:
            self.example = RandomExample1(sign=sign)
        else:
            self.example = RandomExample1(action, sign=sign)

        self.radio_group = QButtonGroup()
        arr = set()
        arr.add(self.example.get_result())
        while len(arr) != 4:
            arr.add(random.randint(-100, 100))

        arr = list(arr)
        random.shuffle(arr)

        self.label = QLabel(self.example.get_without_answer())
        layout.addWidget(self.label)

        for i in range(len(arr)):
            button = QRadioButton(str(arr[i]))
            self.radio_group.addButton(button, id=i)
            layout.addWidget(button)

        self.radio_group.buttonClicked.connect(self.check_complete)

        self.__res = 0

    def isComplete(self):
        if self.radio_group.checkedButton():
            ans = float(self.radio_group.checkedButton().text())

            if ans == self.example.get_result():
                self.__res = 1
            else:
                self.__res = 0

        return self.radio_group.checkedButton() is not None

    def get_action(self):
        return self.example.get_action()

    def get_res(self):
        if self.__res:
            return self.__res
        return 0

    def get_error(self):
        if self.__res == 0:
            return self.example.get_action()
        return None

    @Slot()
    def check_complete(self):
        self.completeChanged.emit()
