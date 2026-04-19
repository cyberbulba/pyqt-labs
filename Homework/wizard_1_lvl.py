import random
import sys

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QGridLayout, QTextEdit, QWizard, QMessageBox, QLineEdit, QWizardPage, QCheckBox
from PySide6.QtWidgets import QPushButton, QDialog, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QRegularExpression
from generate_examples import RandomExample1
from error import ExampleError


class MyWizard(QWizard):
    def __init__(self, level=1):
        super().__init__()
        self.__page_num = 2
        self.__page_count = 1
        self.__add_count_plus = 0
        self.__add_count_minus = 0
        self.__add_count_mult = 0
        self.__add_count_div = 0
        self.__pages = []
        self.__errors = []
        self.__statistic = []

        if level == 1:
            self.sign = 1
        else:
            self.sign = 0

        self.setWindowTitle("Wizard")
        page = ExamplePage(sign=self.sign)
        self.setPage(0, page)

        self.__pages.append(page)

    def reset_wizard(self):
        self.__page_num = 2
        self.__page_count = 1
        self.__add_count_plus = 0
        self.__add_count_minus = 0
        self.__add_count_mult = 0
        self.__add_count_div = 0
        self.__pages.clear()
        self.__errors.clear()
        self.__statistic.clear()

        for page_id in self.pageIds():
            self.removePage(page_id)

        page = ExamplePage(sign=self.sign)
        self.setPage(0, page)
        self.__pages.append(page)

        self.setStartId(0)
        self.restart()

    def nextId(self):
        current_id = self.currentId()

        if current_id < 0 or current_id >= len(self.__pages):
            return -1

        current_page = self.__pages[current_id]

        if not current_page.has_answered():
            page = ExamplePage(sign=self.sign)
            self.__pages.append(page)
            return self.addPage(page)

        res = current_page.get_res()
        action = current_page.get_action()
        self.__errors.append(current_page.get_error())

        self.__statistic.append(res)

        if res == 1:
            self.__page_count += 1
            if self.__page_count > 2:
                self.accept()
                return -1
            page = ExamplePage(sign=self.sign)
            self.__pages.append(page)
            return self.addPage(page)
        else:
            match action:
                case "+":
                    if self.__add_count_plus > 3:
                        self.__page_count += 1
                        print(self.__page_count)
                        if self.__page_count >= 2:
                            self.accept()
                            return -1
                        page = ExamplePage("+", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_plus += 1
                        page = ExamplePage("+", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                case "-":
                    if self.__add_count_minus > 3:
                        self.__page_count += 1
                        print(self.__page_count)
                        if self.__page_count >= 2:
                            self.accept()
                            return -1
                        page = ExamplePage("-", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_minus += 1
                        page = ExamplePage("-", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                case "*":
                    if self.__add_count_mult > 3:
                        self.__page_count += 1
                        print(self.__page_count)
                        if self.__page_count >= 2:
                            self.accept()
                            return -1
                        page = ExamplePage("*", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_mult += 1
                        page = ExamplePage("*", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                case "/":
                    if self.__add_count_div > 3:
                        self.__page_count += 1
                        print(self.__page_count)
                        if self.__page_count >= 2:
                            self.accept()
                            return -1
                        page = ExamplePage("/", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_div += 1
                        page = ExamplePage("/", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)

    def get_statistic(self):
        return sum(list(filter(lambda p: p == 1, self.__statistic))), len(
            list(filter(lambda p: p == 0, self.__statistic))), self.__errors.count("+"), self.__errors.count(
            "-"), self.__errors.count("*"), self.__errors.count("/")


class ExamplePage(QWizardPage):
    def __init__(self, action=None, sign=1):
        super().__init__()
        self.__answered = False
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
            self.__answered = True
            ans = int(self.radio_group.checkedButton().text())

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

    def has_answered(self):
        return self.__answered

    @Slot()
    def check_complete(self):
        self.completeChanged.emit()
