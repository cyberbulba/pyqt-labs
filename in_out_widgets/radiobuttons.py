import sys

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
        self.setWindowTitle("Времена года")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.3)

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
        label.setText("Выберите время года:")

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)


        self.radio_group = QButtonGroup()
        arr = ["Зима", "Весна", "Лето", "Осень"]
        for i in range(len(arr)):
            button = QRadioButton(arr[i])
            self.radio_group.addButton(button, id=i)
            self.layout.addWidget(button)

        self.radio_group.button(0).setChecked(True)
        self.handle_radio_buttons()

        self.radio_group.buttonClicked.connect(self.handle_radio_buttons)



    @Slot()
    def handle_radio_buttons(self):
        year_arr = ["Зима — время покоя и холода: землю укрывает снег, деревья стоят голые, дни короткие, а ночи длинные. Морозные узоры на окнах и новогодние праздники создают особую атмосферу волшебства.",
                    "Весна — время пробуждения природы: тает снег, набухают почки, возвращаются птицы. Дни становятся длиннее, а воздух наполняется свежестью и ароматом первой зелени.",
                    "Лето — сезон тепла и изобилия: солнце светит ярко, деревья покрыты густой листвой, созревают ягоды и фрукты. Люди отдыхают у воды, наслаждаясь длинными светлыми вечерами.",
                    "Осень — пора увядания и уюта: листья окрашиваются в золотые и багряные тона, погода становится прохладнее, небо часто затянуто тучами. Природа готовится к зимнему сну, а люди собирают урожай."]

        self.text_edit.setPlainText(year_arr[self.radio_group.checkedId()])


    def create_text_label(self, text):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        self.layout.addWidget(label)
        label.setText(text)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
