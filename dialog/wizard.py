import sys

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QWizard, QWizardPage, QLineEdit
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout


class MyWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wizard")
        self.addPage(AutorizePage())
        self.addPage(FIOPage())
        self.addPage(CheckboxPage())


class AutorizePage(QWizardPage):
    def __init__(self):
        super().__init__()

        label = QLabel("Hello!")
        layout = QVBoxLayout(self)
        layout.addWidget(label)


class FIOPage(QWizardPage):
    def __init__(self):
        super().__init__()

        label = QLabel("Введите ФИО:")

        self.validator_names = QRegularExpressionValidator(QRegularExpression("^[А-ЯЁA-Z][а-яёa-z]+$"))

        self.family = QLineEdit()
        self.family.setPlaceholderText("Фамилия")
        self.family.setValidator(self.validator_names)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Имя")
        self.name.setValidator(self.validator_names)

        self.fathername = QLineEdit()
        self.fathername.setPlaceholderText("Отчество")
        self.fathername.setValidator(self.validator_names)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.family)
        layout.addWidget(self.name)
        layout.addWidget(self.fathername)


class CheckboxPage(QWizardPage):
    def __init__(self):
        super().__init__()

        label = QLabel("Hello!")
        layout = QVBoxLayout(self)
        layout.addWidget(label)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Запуск Wizard")

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

        button = QPushButton("Запустить Wizard")
        self.layout.addWidget(button)
        self.wizard = MyWizard()

        button.clicked.connect(self.open_wizard)

    def open_wizard(self):
        self.wizard.exec()


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
