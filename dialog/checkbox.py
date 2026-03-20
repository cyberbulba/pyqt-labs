import sys

from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Соглашение")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Вы принимаете соглашение?"))
        self.checkbox = QCheckBox("Соглашаюсь")
        layout.addWidget(self.checkbox)
        self.button = QPushButton("ОК")
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.close_dialog)

    def check_box_clicked(self):
        return self.checkbox.isChecked()

    def close_dialog(self):
        self.close()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Диалоговое окно")

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

        button = QPushButton("Открыть диалоговое окно")
        self.layout.addWidget(button)

        self.res_label = QLabel()
        self.layout.addWidget(self.res_label)

        self.dialog = MyDialog()

        button.clicked.connect(self.open_dialog)
        self.dialog.finished.connect(self.write_agreement)

    def open_dialog(self):
        self.dialog.exec()

    def write_agreement(self):
        if self.dialog.check_box_clicked():
            text = "чекбокс выбран"
        else:
            text = "чекбокс не выбран"

        self.res_label.setText(text)


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
