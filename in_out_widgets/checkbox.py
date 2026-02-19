import sys

from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QCheckBox, QSlider, QSpinBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Магазин")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.5)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        self.layout.addWidget(label)
        label.setText("Выберите продукты:")

        self.checkbox_layout = QVBoxLayout()
        self.layout.addLayout(self.checkbox_layout)

        self.cost_arr = [("виноград", 80), ("сливы", 70), ("яблоки зелёные", 30),
               ("бананы", 50), ("груши", 60)]

        for i in range(len(self.cost_arr)):
            check_box = QCheckBox(self.cost_arr[i][0] + ' - ' + str(self.cost_arr[i][1]) + ' руб/кг')

            spinBox = QSpinBox()
            spinBox.setRange(0, 30)
            spinBox.setSuffix(' кг')

            self.checkbox_layout.addWidget(check_box)
            self.checkbox_layout.addWidget(spinBox)

        button = QPushButton("Посчитать стоимость")
        self.layout.addWidget(button)

        self.label_res = QLabel()
        self.layout.addWidget(self.label_res)

        button.clicked.connect(self.get_cost)

    def handle_checkboxes(self):
        self.cost = 0
        for i in range(0, self.checkbox_layout.count(), 2):
            checkbox = self.checkbox_layout.itemAt(i).widget()
            spinbox = self.checkbox_layout.itemAt(i + 1).widget()

            price = self.cost_arr[i // 2][1]

            if checkbox.isChecked():
                self.cost += price * spinbox.value()

    @Slot()
    def get_cost(self):
        self.handle_checkboxes()

        self.label_res.setText(f'К оплате: {self.cost} руб')


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
