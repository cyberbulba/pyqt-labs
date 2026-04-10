import random
import sys

from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot
from generate_examples import RandomExample1


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Соглашение")

        layout = QVBoxLayout()

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

        self.radio_group.button(0).setChecked(True)


        button = QPushButton("ОК")
        layout.addWidget(button)

        self.setLayout(layout)

        button.clicked.connect(self.close_dialog)

    def check_box_agreed(self):
        return self.__checkbox.isChecked()

    @Slot()
    def close_dialog(self):
        self.accept()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Обучение решению примеров с отрицательными числами")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.height = int(screen_geometry.height())

        self.central_widget = QWidget()
        self.central_widget.setMinimumSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()

        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.button_lvl_1 = QPushButton("Уровень 1")
        self.layout.addWidget(self.button_lvl_1)

        self.button_lvl_2 = QPushButton("Уровень 2")
        self.layout.addWidget(self.button_lvl_2)

        self.button_lvl_3 = QPushButton("Уровень 3")
        self.layout.addWidget(self.button_lvl_3)

        self.dialog = MyDialog()
        self.button_lvl_1.clicked.connect(self.open_dialog)

    @Slot()
    def open_dialog(self):
        self.dialog.exec()


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
