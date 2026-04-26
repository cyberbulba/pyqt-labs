import random
import sys

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QGridLayout, QTextEdit, QWizard, QMessageBox, QLineEdit, QWizardPage, QCheckBox
from PySide6.QtWidgets import QPushButton, QDialog, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QRegularExpression, Qt
from generate_examples import RandomExample1
from example_page import ExamplePage


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

        self.setButtonLayout([
            QWizard.NextButton,
            QWizard.CancelButton
        ])

        page = ExamplePage(sign=self.sign)
        self.setPage(0, page)

        self.__pages.append(page)

    def reset_wizard(self):
        """метод выполняет обновление wizard перед новым его запуском"""
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
        """метод настраивает переходы между страницами wizard"""
        current_id = self.currentId()

        if current_id < 0 or current_id >= len(self.__pages):
            return -1

        current_page = self.__pages[current_id]

        if not current_page.isComplete():
            return current_id

        res = current_page.get_res()
        action = current_page.get_action()
        self.__errors.append(current_page.get_error())

        self.__statistic.append(res)

        if res == 1:
            self.__page_count += 1
            if self.__page_count > self.__page_num:
                self.accept()
                return -1
            page = ExamplePage(sign=self.sign)
            self.__pages.append(page)
            return self.addPage(page)
        else:
            match action:
                case "+":
                    if self.__add_count_plus >= 3:
                        self.__page_count += 1
                        if self.__page_count > self.__page_num:
                            self.accept()
                            return -1
                        page = ExamplePage(sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_plus += 1
                        page = ExamplePage("+", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                case "-":
                    if self.__add_count_minus >= 3:
                        self.__page_count += 1
                        if self.__page_count > self.__page_num:
                            self.accept()
                            return -1
                        page = ExamplePage(sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_minus += 1
                        page = ExamplePage("-", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                case "*":
                    if self.__add_count_mult >= 3:
                        self.__page_count += 1
                        if self.__page_count > self.__page_num:
                            self.accept()
                            return -1
                        page = ExamplePage(sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_mult += 1
                        page = ExamplePage("*", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                case "/":
                    if self.__add_count_div >= 3:
                        self.__page_count += 1
                        if self.__page_count > self.__page_num:
                            self.accept()
                            return -1
                        page = ExamplePage(sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)
                    else:
                        self.__add_count_div += 1
                        page = ExamplePage("/", sign=self.sign)
                        self.__pages.append(page)
                        return self.addPage(page)

    def get_statistic(self):
        """метод, необходимый для получения статистики прохождения теста, находящегося в wizard"""
        return sum(list(filter(lambda p: p == 1, self.__statistic))), len(
            list(filter(lambda p: p == 0, self.__statistic))), self.__errors.count("+"), self.__errors.count(
            "-"), self.__errors.count("*"), self.__errors.count("/")
