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
    def __init__(self):
        super().__init__()
        self.__page_num = 2
        self.__default_index = 0
        self.__add_index = self.__page_num

        self.setWindowTitle("Wizard")

        self.pages = []

        for _ in range(self.__page_num):
            page = ExamplePage()
            self.addPage(page)
            self.pages.append(page)

        for _ in range(3):
            page = ExamplePage()
            self.addPage(page)
            self.pages.append(page)

    def nextId(self):
        current_id = self.currentId()
        print(current_id)
        print(self.__default_index)
        if current_id >= self.__page_num:
            if self.pages[current_id].get_res() == 0:
                self.__add_index += 1
                if self.__add_index >= len(self.pages) - 1:
                    self.accept()
                return self.__add_index
            else:
                self.__default_index += 1
                if self.__default_index == self.__page_num:
                    self.accept()
                return self.__default_index
        else:
            if self.pages[current_id].get_res() == 0:
                return self.__add_index
            else:
                if self.__default_index >= self.__page_num - 1:
                    self.accept()
                self.__default_index += 1
                return self.__default_index

    # def accept(self):
    #     QMessageBox.information(None, "Wizard", "Wizard is accepted")
    #     print(list(map(lambda page: page.get_res(), self.pages)))
    #     print(*filter(lambda x: x is not None, map(lambda page: page.get_errors(), self.pages)))
    #     super(MyWizard, self).accept()


class ExamplePage(QWizardPage):
    def __init__(self):
        super().__init__()

        label = QLabel("Решите пример:")

        layout = QVBoxLayout(self)
        layout.addWidget(label)

        self.example = RandomExample1()

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
            ans = int(self.radio_group.checkedButton().text())

            if ans == self.example.get_result():
                self.__res = 1

        return self.radio_group.checkedButton() is not None

    def validate_page(self):
        ans = int(self.radio_group.checkedButton().text())

        if ans == self.example.get_result():
            self.__res = 1

    def get_res(self):
        if self.__res:
            return self.__res
        return 0

    def get_errors(self):
        if self.__res == 0:
            return ExampleError(self.example.get_action())
        return None

    @Slot()
    def check_complete(self):
        self.completeChanged.emit()


# class MyDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Соглашение")
#
#         layout = QVBoxLayout()
#
#         self.example = RandomExample1()
#
#         self.radio_group = QButtonGroup()
#         arr = [self.example.get_result(), random.randint(-100, -1), random.randint(-100, -1), random.randint(-100, -1)]
#         random.shuffle(arr)
#
#         self.label = QLabel(self.example.get_without_answer())
#         layout.addWidget(self.label)
#
#         for i in range(len(arr)):
#             button = QRadioButton(str(arr[i]))
#             self.radio_group.addButton(button, id=i)
#             layout.addWidget(button)
#
#         self.radio_group.button(0).setChecked(True)
#
#
#         button = QPushButton("ОК")
#         layout.addWidget(button)
#
#         self.setLayout(layout)
#
#         button.clicked.connect(self.close_dialog)
#
#     def check_box_agreed(self):
#         return self.__checkbox.isChecked()
#
#     @Slot()
#     def close_dialog(self):
#         self.accept()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Обучение решению примеров с отрицательными числами")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.height = int(screen_geometry.height())
        self.width = int(screen_geometry.width())

        self.central_widget = QWidget()
        self.central_widget.setMinimumSize(self.width, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()

        self.move(window_geometry.topLeft())

        self.layout = QGridLayout(self.central_widget)

        self.button_lvl_1 = QPushButton("Уровень 1")
        self.layout.addWidget(self.button_lvl_1, 0, 5)

        self.button_lvl_2 = QPushButton("Уровень 2")
        self.layout.addWidget(self.button_lvl_2, 1, 5)

        self.button_lvl_3 = QPushButton("Уровень 3")
        self.layout.addWidget(self.button_lvl_3, 2, 5)

        question_label = QLabel("Справочные материалы по действиям с отрицательными числами")
        self.layout.addWidget(question_label, 0, 0, 1, 4)

        self.button_plus = QPushButton("+")
        self.layout.addWidget(self.button_plus, 1, 0)
        self.button_plus.clicked.connect(self.handle_plus)

        self.button_plus = QPushButton("-")
        self.layout.addWidget(self.button_plus, 1, 1)

        self.button_plus = QPushButton("*")
        self.layout.addWidget(self.button_plus, 1, 2)

        self.button_plus = QPushButton("/")
        self.layout.addWidget(self.button_plus, 1, 3)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout.addWidget(self.textEdit, 2, 0, 1, 4)

        self.wizard = MyWizard()

        self.button_lvl_1.clicked.connect(self.open_wizard)

    #     self.dialog = MyDialog()
    #     self.button_lvl_1.clicked.connect(self.open_dialog)
    #
    # @Slot()
    # def open_dialog(self):
    #     self.dialog.exec()
    @Slot()
    def open_wizard(self):
        self.wizard.exec()

    @Slot()
    def handle_plus(self):
        self.textEdit.setText("Рассмотрим сложение с отрицательным числом:\n "
                              "1. Если число, к которому прибавляем положительное, пример -3 + 5, \n"
                              "тогда чтобы получить ответ, необходимо вычесть из него отрицательное число, то есть 5 - 3 = 2\n"
                              "2. Если число, к которому прибавляем отрицательное, например -3 - 5, то необходимо сложить модули\n"
                              "этих чисел: 3 + 5 = 8 и заменить знак на противоположный, таким образом -3 - 5 = -8\n"
                              "3. Если число, к которому прибавляем является 0, например -3 + 0 то в ответ следует записать само отрицательное число: -3 + 0 = -3\n")


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
