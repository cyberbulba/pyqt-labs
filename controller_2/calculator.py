import sys
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QPushButton, QLineEdit, QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Signal, Slot, QObject, Qt


# Модель калькулятора
class CalculatorModel(QObject):
    result_updated = Signal(str)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()

    def calculate(self, operation, num1, num2):
        try:
            if operation == '+':
                result = num1 + num2
                self.result_updated.emit(f"{num1} + {num2} = {result}")
            elif operation == '-':
                result = num1 - num2
                self.result_updated.emit(f"{num1} - {num2} = {result}")
            elif operation == '*':
                result = num1 * num2
                self.result_updated.emit(f"{num1} * {num2} = {result}")
            elif operation == '/':
                if num2 == 0:
                    raise ValueError("Деление на ноль")
                result = num1 // num2
                self.result_updated.emit(f"{num1} // {num2} = {result}")
            elif operation == '**':
                result = num1 ** num2
                self.result_updated.emit(f"{num1}<sup>{num2}</sup> = {result}")
            else:
                raise ValueError("Неизвестная операция")
        except Exception as e:
            self.error_occurred.emit(str(e))


class CalculatorController(QObject):
    operation_requested = Signal(str, int, int)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.model.result_updated.connect(self.view.update_result)
        self.model.error_occurred.connect(self.view.show_error)

        self.operation_requested.connect(self.model.calculate)

        self.view.plus_button.clicked.connect(lambda: self.on_operation_clicked('+'))
        self.view.minus_button.clicked.connect(lambda: self.on_operation_clicked('-'))
        self.view.mult_button.clicked.connect(lambda: self.on_operation_clicked('*'))
        self.view.division_button.clicked.connect(lambda: self.on_operation_clicked('/'))
        self.view.power_button.clicked.connect(lambda: self.on_operation_clicked('**'))

    @Slot()
    def on_operation_clicked(self, operation):
        num1 = self.view.get_num1()
        num2 = self.view.get_num2()

        if num1 is None or num2 is None:
            self.model.error_occurred.emit("Введены неправильные числа!")
            return

        self.operation_requested.emit(operation, num1, num2)


# Вид калькулятора
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.model = CalculatorModel()
        self.controller = CalculatorController(self.model, self)

    def initUI(self):
        self.setWindowTitle("Калькулятор")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.height = int(screen_geometry.height() * 0.6)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.create_text_label("Введите первое число:")
        self.line_edit1 = QLineEdit()
        self.layout.addWidget(self.line_edit1)
        self.validator = QIntValidator(self)
        self.line_edit1.setValidator(self.validator)

        self.create_text_label("Введите второе число:")
        self.line_edit2 = QLineEdit()
        self.layout.addWidget(self.line_edit2)
        self.line_edit2.setValidator(self.validator)

        self.plus_button = QPushButton("+")
        self.layout.addWidget(self.plus_button)

        self.minus_button = QPushButton("-")
        self.layout.addWidget(self.minus_button)

        self.mult_button = QPushButton("*")
        self.layout.addWidget(self.mult_button)

        self.division_button = QPushButton("/")
        self.layout.addWidget(self.division_button)

        self.power_button = QPushButton("**")
        self.layout.addWidget(self.power_button)

        self.create_text_label("Результат:")

        self.rez_label = QLabel()
        self.layout.addWidget(self.rez_label)

    def get_num1(self):
        text = self.line_edit1.text()
        state, _, _ = self.validator.validate(text, 0)
        if state == QIntValidator.State.Acceptable:
            return int(text)
        return None

    def get_num2(self):
        text = self.line_edit2.text()
        state, _, _ = self.validator.validate(text, 0)
        if state == QIntValidator.State.Acceptable:
            return int(text)
        return None

    @Slot(str)
    def update_result(self, result_text):
        self.rez_label.setText(result_text)

    @Slot(str)
    def show_error(self, error_message):
        self.rez_label.setText(error_message)

    def create_text_label(self, text):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)
        label.setText(text)


def main():
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
