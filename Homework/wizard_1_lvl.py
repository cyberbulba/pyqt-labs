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
        self.__statistic = []

        if level == 1:
            self.sign = 1
        else:
            self.sign = 0

        self.setWindowTitle("Wizard")
        page = ExamplePage(sign=self.sign)
        self.setPage(0, page)

        self.__pages.append(page)

        # self.pages = []
        #
        # for _ in range(self.__page_num):
        #     page = ExamplePage()
        #     self.addPage(page)
        #     self.pages.append(page)
        #
        # for _ in range(3):
        #     page = ExamplePage()
        #     self.addPage(page)
        #     self.pages.append(page)

        # self.setOptions(QWizard.NoBackButtonOnStartPage | QWizard.NoBackButtonOnLastPage)

    # def nextId(self):
    #     current_id = self.currentId()
    #     current_page = self.__pages[current_id]
    #
    #     print(f'count:{self.__page_count}')
    #     print(f'+:{self.__add_count_plus}')
    #
    #     if not current_page.has_answered():
    #         page = ExamplePage()
    #         self.__pages.append(page)
    #         return self.addPage(page)
    #
    #     res = current_page.get_res()
    #     self.__statistic.append(res)
    #
    #     if res == 1:
    #         self.__page_count += 1
    #         if self.__page_count > 2:
    #             self.accept()
    #         page = ExamplePage()
    #         self.__pages.append(page)
    #         return self.addPage(page)
    #     else:
    #         if self.__add_count_plus > 3:
    #             self.__page_count += 1
    #             print(self.__page_count)
    #             if self.__page_count >= 2:
    #                 self.accept()
    #             page = ExamplePage()
    #             self.__pages.append(page)
    #             return self.addPage(page)
    #         else:
    #             self.__add_count_plus += 1
    #             page = ExamplePage()
    #             self.__pages.append(page)
    #             return self.addPage(page)

    def nextId(self):
        current_id = self.currentId()
        current_page = self.__pages[current_id]

        if not current_page.has_answered():
            page = ExamplePage(sign=self.sign)
            self.__pages.append(page)
            return self.addPage(page)

        res = current_page.get_res()
        action = current_page.get_action()

        print(f'count:s{self.__page_count}')
        print(
            f'+:{self.__add_count_plus}  -:{self.__add_count_minus} *:{self.__add_count_mult} /:{self.__add_count_div}')

        self.__statistic.append(res)
        print(self.__statistic)

        if res == 1:
            self.__page_count += 1
            if self.__page_count > 2:
                self.accept()
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
                            return self.accept()
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
                            return self.accept()
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
            list(filter(lambda p: p == 0, self.__statistic)))


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
        arr = [self.example.get_result(), random.randint(-100, -1), random.randint(-100, -1), random.randint(-100, -1)]
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

        return self.radio_group.checkedButton() is not None

    def get_action(self):
        return self.example.get_action()

    def get_res(self):
        if self.__res:
            return self.__res
        return 0

    def get_errors(self):
        if self.__res == 0:
            return ExampleError(self.example.get_action())
        return None

    def has_answered(self):
        return self.__answered

    @Slot()
    def check_complete(self):
        self.completeChanged.emit()
