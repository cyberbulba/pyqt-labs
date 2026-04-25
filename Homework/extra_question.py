from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QAbstractItemModel, Slot, Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QLineEdit
from generate_examples import RandomExample1


class QuestionView(QWidget):
    def __init__(self):
        super().__init__()
        self.model = None

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.label = QLabel("Выберите действие (кнопки слева):")
        self.layout.addWidget(self.label)

        self.__spinbox = QSpinBox()
        self.__spinbox.setMinimum(-10000)
        self.__spinbox.setMaximum(10000)
        self.layout.addWidget(self.__spinbox)

        self.check_button = QPushButton("Проверить ответ")
        self.check_button.clicked.connect(self.set_result)

        self.layout.addWidget(self.check_button)
        self.res_line = QLabel()
        self.layout.addWidget(self.res_line)

    def setModel(self, model):
        self.model = model
        self.model.exampleChanged.connect(self.set_example)

    @Slot()
    def set_example(self):
        self.label.setText(f"Решите пример: {self.model.get_example()}")

    @Slot()
    def set_result(self):
        if self.model.get_example() is not None:
            self.res_line.setText(f"Ваш ответ {self.__spinbox.value()}, правильный: {self.model.get_answer()}")


class QuestionModel(QAbstractItemModel):
    exampleChanged = Signal()

    def __init__(self):
        super().__init__()
        self.example = None

    def generate_new_question(self, action):
        self.example = RandomExample1(action, 0)
        self.exampleChanged.emit()

    def get_example(self):
        if self.example is not None:
            return self.example.get_without_answer()
        return None

    def get_answer(self):
        if self.example is not None:
            return self.example.get_result()
        return None
