import sys

from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Расписание ИВТ")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.7)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Вкладка 1")
        self.tabs.addTab(self.tab2, "Вкладка 2")
        self.tabs.addTab(self.tab3, "Вкладка 3")

        self.tabs.setFixedSize(self.height, self.height)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        arr1 = [[["нет пары", "нет пары"], ["нет пары", "Ин яз пр"]], [["Диффуры пр"], ["Компл. анализ пр"]],
                [["Практикум на ЭВМ\n по языкам программирования"], ["Диффуры пр"]],
                [["нет пары"], ["Практикум на ЭВМ\n по языкам программирования"]]]

        arr2 = [["Диффуры лекц"], ["Языки и методы программирования л"],
                [["Компл. анализ пр"], ["Основы тестирования ПО пр"]],
                [["Физика пр"], ["нет пары"]], [["Физика пр", "нет пары"], ["нет пары", "нет пары"]]]

        self.layout = QGridLayout(self.tab1)

        self.layout.addWidget(QLabel('День недели'), 0, 0)
        self.layout.addWidget(QLabel('Числитель/знаменатель'), 0, 1)
        self.layout.addWidget(QLabel('ИВТ-21БО'), 0, 2)
        self.layout.addWidget(QLabel('ИВТ-22БО'), 0, 3)

        add = self.add_day("Понедельник", arr1, 1)
        self.add_day("Вторник", arr2, add)

    def add_day(self, day, arr1, add):  # переменная добавки на случай, если пара делится на числитель и знаменатель
        for i in range(len(arr1)):
            add_flag = 0
            flag = 0
            if len(arr1[i]) == 1:
                self.layout.addWidget(QLabel(arr1[i][0]), i + add, 2, 1, 2)
                self.layout.addWidget(QLabel("Числитель + знаменатель"), i + add, 1)
                self.layout.addWidget(QLabel(day), i + add, 0)

            else:
                if len(arr1[i][0]) == 2:  # случай с числителем и знаменателем
                    self.layout.addWidget(QLabel("Числитель"), i + add, 1)
                    self.layout.addWidget(QLabel("Знаменатель"), i + add + 1, 1)
                    self.layout.addWidget(QLabel(day), i + add + 1, 0)
                    flag = 1
                else:
                    self.layout.addWidget(QLabel("Числитель + знаменатель"), i + add, 1)

                self.layout.addWidget(QLabel(day), i + add, 0)

                for j in range(len(arr1[i])):
                    if flag:
                        self.layout.addWidget(QLabel(arr1[i][j][0]), i + add, j + 2)
                        self.layout.addWidget(QLabel(arr1[i][j][1]), i + add + 1, j + 2)
                        add_flag = 1

                    else:
                        self.layout.addWidget(QLabel(arr1[i][j][0]), i + add, j + 2)
                if add_flag:  # увеличиваем добавку если есть числитель и знаменатель
                    add += 2
        return add + len(arr1)

        # self.layout = QVBoxLayout(self.central_widget)
        #
        # label = QLabel()
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        # self.layout.addWidget(label)
        # label.setText("Выберите время года:")
        #
        # self.text_edit = QTextEdit()
        # self.layout.addWidget(self.text_edit)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
