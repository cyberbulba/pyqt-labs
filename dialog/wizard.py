import sys

from PySide6.QtCore import QRegularExpression, Slot
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QPushButton, QDialog, QCheckBox, QWizard, QWizardPage, QLineEdit, QTextEdit, QMessageBox
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout


class MyWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wizard")
        self.addPage(AutorizePage())
        self.addPage(FIOPage())
        self.__page3 = CheckboxPage()
        self.addPage(self.__page3)

    def accept(self):
        QMessageBox.information(None, "Wizard", "Wizard is accepted")
        super(MyWizard, self).accept()

    def get_selected_items(self):
        return self.__page3.get_selected_items()

    def get_text(self):
        user_info_string = "Пользователь ввёл: \n"
        user_info_string += f'Логин: {self.field("loginField")} \n'
        user_info_string += f'Пароль: {self.field("passwordField")} \n'
        user_info_string += f'Фамилия: {self.field("familyField")} \n'
        user_info_string += f'Имя: {self.field("nameField")} \n'
        user_info_string += f'Отчество: {self.field("fathernameField")} \n'
        user_info_string += f'Пользователю интересны: {self.get_selected_items()} \n'

        if self.field("spamField"):
            user_info_string += f'Пользователь согласен на рассылку\n'
        else:
            user_info_string += f'Пользователь не согласен на рассылку\n'

        return user_info_string


class AutorizePage(QWizardPage):
    def __init__(self):
        super().__init__()

        self.__validator_login_password = QRegularExpressionValidator(
            QRegularExpression("[a-zа-яёA-ZА-ЯЁ0-9]+$"))

        label = QLabel("Вход в систему:")

        layout = QVBoxLayout(self)
        layout.addWidget(label)

        self.__login = QLineEdit()
        self.__login.setPlaceholderText("Логин (буквы, цифры)")
        self.__login.setValidator(self.__validator_login_password)
        self.__login.textChanged.connect(self.check_complete)
        self.registerField("loginField", self.__login)

        self.__password = QLineEdit()
        self.__password.setPlaceholderText("Пароль (буквы, цифры)")
        self.__password.setValidator(self.__validator_login_password)
        self.__password.textChanged.connect(self.check_complete)
        self.registerField("passwordField", self.__password)

        layout.addWidget(self.__login)
        layout.addWidget(self.__password)

        self.__error_text = QTextEdit()
        self.__error_text.setReadOnly(True)
        layout.addWidget(self.__error_text)

    def isComplete(self):
        error_string = ""

        state_login, _, _ = self.__validator_login_password.validate(self.__login.text(), 0)
        state_password, _, _ = self.__validator_login_password.validate(self.__password.text(), 0)

        if state_login != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильный логин!\n"

        if state_password != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильный пароль!\n"
        if not error_string:
            self.__error_text.setText("Все данные корректны")
        else:
            self.__error_text.setText(error_string)

        return (state_login == QRegularExpressionValidator.State.Acceptable and
                state_password == QRegularExpressionValidator.State.Acceptable)

    @Slot()
    def check_complete(self):
        self.completeChanged.emit()


class FIOPage(QWizardPage):
    def __init__(self):
        super().__init__()

        label = QLabel("Введите ФИО:")

        self.__validator_names = QRegularExpressionValidator(QRegularExpression("^[А-ЯЁA-Z][а-яёa-z]+$"))

        self.__family = QLineEdit()
        self.__family.setPlaceholderText("Фамилия")
        self.__family.setValidator(self.__validator_names)
        self.__family.textChanged.connect(self.check_complete)
        self.registerField("familyField", self.__family)

        self.__name = QLineEdit()
        self.__name.setPlaceholderText("Имя")
        self.__name.setValidator(self.__validator_names)
        self.__name.textChanged.connect(self.check_complete)
        self.registerField("nameField", self.__name)

        self.__fathername = QLineEdit()
        self.__fathername.setPlaceholderText("Отчество")
        self.__fathername.setValidator(self.__validator_names)
        self.__fathername.textChanged.connect(self.check_complete)
        self.registerField("fathernameField", self.__fathername)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.__family)
        layout.addWidget(self.__name)
        layout.addWidget(self.__fathername)

        self.__error_text = QTextEdit()
        self.__error_text.setReadOnly(True)
        layout.addWidget(self.__error_text)

    def isComplete(self):
        error_string = ""

        state_family, _, _ = self.__validator_names.validate(self.__family.text(), 0)
        state_name, _, _ = self.__validator_names.validate(self.__name.text(), 0)
        state_fathername, _, _ = self.__validator_names.validate(self.__fathername.text(), 0)

        if state_family != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильная фамилия!\n"

        if state_name != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильное имя!\n"

        if state_fathername != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильное отчество!\n"

        if not error_string:
            self.__error_text.setText("Все данные корректны")
        else:
            self.__error_text.setText(error_string)

        return (state_family == QRegularExpressionValidator.State.Acceptable and
                state_name == QRegularExpressionValidator.State.Acceptable and
                state_fathername == QRegularExpressionValidator.State.Acceptable)

    @Slot()
    def check_complete(self):
        self.completeChanged.emit()


class CheckboxPage(QWizardPage):
    def __init__(self):
        super().__init__()

        label = QLabel("Что Вас интересует?")
        layout = QVBoxLayout(self)
        layout.addWidget(label)

        self.__checkboxes = {}

        items = ["Видеокарты", "Процессоры", "БП", "ОЗУ", "Диски", "Мат. платы"]
        for item in items:
            checkbox = QCheckBox(item)
            layout.addWidget(checkbox)
            self.__checkboxes[item] = checkbox

        layout.addWidget(QLabel("Вы согласны на рассылку?"))
        self.__spam_checkbox = QCheckBox("Я согласен на рассылку")
        layout.addWidget(self.__spam_checkbox)

        self.registerField("spamField", self.__spam_checkbox)

    def get_selected_items(self):
        selected_items = []

        for item in self.__checkboxes.keys():
            if self.__checkboxes[item].isChecked():
                selected_items.append(item)

        return ", ".join(selected_items) if selected_items else "Ничего не выбрано"


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
        self.wizard.accepted.connect(self.print_user_data)

        self.res_text = QTextEdit()
        self.layout.addWidget(self.res_text)
        self.res_text.setReadOnly(True)

    @Slot()
    def open_wizard(self):
        self.wizard.exec()

    @Slot()
    def print_user_data(self):
        user_info_string = self.wizard.get_text()

        self.res_text.setText(user_info_string)


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
