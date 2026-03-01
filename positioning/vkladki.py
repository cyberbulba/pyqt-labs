import sys

from PySide6.QtCore import QRegularExpression, QMimeData, QPoint
from PySide6.QtGui import QRegularExpressionValidator, QDrag
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QFormLayout, QLineEdit
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QPushButton, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class DragLabel(QLabel):
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            drag.setMimeData(QMimeData())
            drag.exec(Qt.MoveAction)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_flag = 0
        self.move_flag = 0
        self.drag_offset = QPoint(0, 0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Вкладки")

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

        arr2 = [["Диффуры л"], ["Языки и методы программирования л"],
                [["Компл. анализ пр"], ["Основы тестирования ПО пр"]],
                [["Физика пр"], ["нет пары"]], [["Физика пр", "нет пары"], ["нет пары", "нет пары"]]]

        self.layout = QGridLayout(self.tab1)

        self.layout.addWidget(QLabel('День недели'), 0, 0)
        self.layout.addWidget(QLabel('Номер пары'), 0, 1)
        self.layout.addWidget(QLabel('Числитель/знаменатель'), 0, 2)
        self.layout.addWidget(QLabel('ИВТ-21БО'), 0, 3)
        self.layout.addWidget(QLabel('ИВТ-22БО'), 0, 4)

        add = self.add_day("Понедельник", arr1, 1)
        self.add_day("Вторник", arr2, add)

        self.layout2 = QVBoxLayout()
        form_layout = QFormLayout(self.tab2)
        self.layout2.addLayout(form_layout)

        self.validator_names = QRegularExpressionValidator(QRegularExpression("^[А-ЯЁA-Z][а-яёa-z]+$"))

        names = ["Фамилия", "Имя", "Отчество"]
        self.name_line_edits = []
        for name in names:
            name_line_edit = QLineEdit()
            self.name_line_edits.append(name_line_edit)
            form_layout.addRow(name, name_line_edit)
            name_line_edit.setValidator(self.validator_names)

        self.validator_email = QRegularExpressionValidator(
            QRegularExpression("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$"))
        self.email_line_edit = QLineEdit()
        form_layout.addRow("Почта:", self.email_line_edit)
        self.email_line_edit.setValidator(self.validator_email)

        self.validator_number = QRegularExpressionValidator(
            QRegularExpression("^(\\+7|8)\\d{10}$"))
        self.number_line_edit = QLineEdit()
        form_layout.addRow("Телефон (без ввода дефисов):", self.number_line_edit)
        self.number_line_edit.setValidator(self.validator_number)

        form_layout.addRow(QLabel("Выберите интересные Вам темы:"))

        items = ["Видеокарты", "Процессоры", "БП", "ОЗУ", "Диски", "Мат. платы"]
        for item in items:
            form_layout.addRow(QCheckBox(item))

        form_layout.addRow(QLabel("Согласны ли Вы на обработку ваших данных?"))
        self.personal_data = QCheckBox("Я согласен(а) на обработку персональных данных")
        form_layout.addRow(self.personal_data)
        form_layout.addRow(QCheckBox("Я согласен(а) на получение рассылок по почте"))

        self.button = QPushButton("Зарегестрироваться")
        form_layout.addRow(self.button)
        self.button.clicked.connect(self.validate_form)

        self.error_text = QTextEdit()
        form_layout.addRow(self.error_text)
        self.error_text.setReadOnly(True)
        self.tab3.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.position()

        if pos.y() > self.height // 2 and self.move_flag == 0:
            self.move_label.move(pos.x(), pos.y())
            self.move_flag = 1

        e.accept()

    def mousePressEvent(self, event):
        if self.tabs.currentIndex() == 2:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.widget_flag == 0:
                    if event.position().y() < self.height // 2:
                        if self.widget_flag == 0:
                            self.move_label = DragLabel(self.tab3)
                            self.move_label.setText("Hello world")
                            self.move_label.show()
                            self.move_label.move(int(event.position().x()), int(event.position().y()))

                            self.widget_flag = 1

    @Slot()
    def validate_form(self):
        error_string = ''
        if not self.personal_data.isChecked():
            error_string += "Вы не согласны на обработку данных!\n"

        state_num, _, _ = self.validator_number.validate(self.number_line_edit.text(), 0)
        state_email, _, _ = self.validator_email.validate(self.email_line_edit.text(), 0)
        state_family, _, _ = self.validator_names.validate(self.name_line_edits[0].text(), 0)
        state_name, _, _ = self.validator_names.validate(self.name_line_edits[1].text(), 0)
        state_fathername, _, _ = self.validator_names.validate(self.name_line_edits[2].text(), 0)

        if state_num != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильный номер телефона!\n"

        if state_email != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильная почта!\n"

        if state_family != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильная фамилия!\n"

        if state_name != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильное имя!\n"

        if state_fathername != QRegularExpressionValidator.State.Acceptable:
            error_string += "Неправильное отчество!\n"

        if not error_string:
            self.error_text.setText("Успешная регистрация!")
        else:
            self.error_text.setText(error_string)

    def add_day(self, day, schedule, row_offset):
        pair_num = 1
        current_row = row_offset

        for pair in schedule:
            is_common_pair = len(pair) == 1  # тип пары
            has_numerator_denominator = len(pair) > 1 and len(pair[0]) == 2

            if is_common_pair:  # случай где 1 пара на 2 потока
                self.layout.addWidget(QLabel(day), current_row, 0)
                self.layout.addWidget(QLabel(str(pair_num)), current_row, 1)
                self.layout.addWidget(QLabel("Числитель + знаменатель"), current_row, 2)
                self.layout.addWidget(QLabel(pair[0]), current_row, 3, 1, 2)

                current_row += 1
                pair_num += 1

            elif has_numerator_denominator:  # случай где пара с числителем или знаменателем на 1 группу
                for j, subject in enumerate(pair):
                    self.layout.addWidget(QLabel(day), current_row, 0)
                    self.layout.addWidget(QLabel(str(pair_num)), current_row, 1)
                    self.layout.addWidget(QLabel("Числитель" if j == 0 else "Знаменатель"), current_row, 2)
                    self.layout.addWidget(QLabel(subject[0]), current_row, 3)
                    self.layout.addWidget(QLabel(subject[1]), current_row, 4)
                    current_row += 1

                pair_num += 1

            else:  # пара на 1 группу с числителем и знаменателем
                self.layout.addWidget(QLabel(day), current_row, 0)
                self.layout.addWidget(QLabel(str(pair_num)), current_row, 1)
                self.layout.addWidget(QLabel("Числитель + знаменатель"), current_row, 2)

                for j, subject in enumerate(pair):
                    self.layout.addWidget(QLabel(subject[0]), current_row, j + 3)

                current_row += 1
                pair_num += 1

        return current_row


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
