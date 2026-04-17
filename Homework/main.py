import random
import sys

from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QGridLayout, QTextEdit, QWizard, QMessageBox, QLineEdit, QWizardPage, QCheckBox, QListView
from PySide6.QtWidgets import QPushButton, QDialog, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot, QRegularExpression
from generate_examples import RandomExample1
from error import ExampleError
from wizard_1_lvl import MyWizard
from list_model import ListModel


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
        self.num = 0

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

        self.button_minus = QPushButton("-")
        self.layout.addWidget(self.button_minus, 1, 1)
        self.button_minus.clicked.connect(self.handle_minus)

        self.button_mult = QPushButton("*")
        self.layout.addWidget(self.button_mult, 1, 2)
        self.button_mult.clicked.connect(self.handle_mult)

        self.button_div = QPushButton("/")
        self.layout.addWidget(self.button_div, 1, 3)
        self.button_div.clicked.connect(self.handle_div)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout.addWidget(self.textEdit, 2, 0, 1, 4)

        self.model = ListModel()
        view = QListView()
        view.setModel(self.model)
        self.layout.addWidget(view, 3, 0, 1, 4)

        self.wizard = MyWizard()

        self.button_lvl_1.clicked.connect(self.open_wizard)

        self.wizard.accepted.connect(self.set_new_result)

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

    @Slot()
    def handle_minus(self):
        self.textEdit.setText("Рассмотрим вычитание из отрицательного числа:\n "
                              "1. Если из отрицательного числа вычитаем положительное, пример -3 - 5, \n"
                              "тогда необходимо сложить модули чисел: 3 + 5 = 8 и поставить знак минус: -3 - 5 = -8\n"
                              "2. Если из числа вычитаем отрицательное, например -3 - (-5), то два минуса дают плюс, \n"
                              "заменяем вычитание на сложение: -3 + 5 = 2\n"
                              "3. Если вычитаемое равно 0, например -3 - 0, то число не изменяется: -3 - 0 = -3\n")

    @Slot()
    def handle_mult(self):
        self.textEdit.setText("Рассмотрим умножение с отрицательным числом:\n "
                              "1. Если отрицательное число умножаем на отрицательное, пример -3 * (-5), \n"
                              "тогда минус на минус дает плюс. Перемножаем модули: 3 * 5 = 15, результат: 15\n"
                              "2. Если отрицательное число умножаем на положительное, например -3 * 5, то результат будет отрицательным: \n"
                              "3 * 5 = 15, и заменить знак на противоположный: -15\n"
                              "3. Если один из множителей равен 0, например -3 * 0, то произведение равно 0\n")

    @Slot()
    def handle_div(self):
        self.textEdit.setText("Рассмотрим деление с отрицательным числом:\n "
                              "1. Если отрицательное число делим на отрицательное, пример -10 / (-2), \n"
                              "тогда минус на минус дает плюс. Делим модули: 10 / 2 = 5, результат: 5\n"
                              "2. Если отрицательное число делим на положительное, например -10 / 2, то результат будет отрицательным: \n"
                              "10 / 2 = 5, и заменить знак на противоположный: -5\n"
                              "3. Если делимое равно 0, например 0 / (-5), то частное равно 0\n")

    @Slot()
    def set_new_result(self):
        self.num += 1
        self.model.addRow(
            f'Тест {self.num}: {self.wizard.get_statistic()[0]} из {self.wizard.get_statistic()[0] + self.wizard.get_statistic()[1]} правильных ответов')

        self.wizard = MyWizard()
        self.wizard.accepted.connect(self.set_new_result)


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
