from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QAbstractItemModel, Slot, Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QLineEdit
from generate_examples import RandomExample1


class QuestionView(QWidget):
    def __init__(self):
        super().__init__()
        self.__model = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.__label = QLabel("Выберите действие (кнопки слева):")
        layout.addWidget(self.__label)

        self.__spinbox = QSpinBox()
        self.__spinbox.setMinimum(-10000)
        self.__spinbox.setMaximum(10000)
        layout.addWidget(self.__spinbox)

        check_button = QPushButton("Проверить ответ")
        check_button.clicked.connect(self.set_result)

        layout.addWidget(check_button)
        self.__res_line = QLabel()
        layout.addWidget(self.__res_line)

    def setModel(self, model):
        """метод, устанавливающий модель для вида"""
        self.__model = model
        self.__model.exampleChanged.connect(self.set_example)

    @Slot()
    def set_example(self):
        """метод, устанавливающий в label текст примера"""
        self.__label.setText(f"Решите пример: {self.__model.get_example()}")

    @Slot()
    def set_result(self):
        """метод, который устанавливает в label для проверки ответа полученный и правильный ответы"""
        if self.__model.get_example() is not None:
            self.__res_line.setText(f"Ваш ответ {self.__spinbox.value()}, правильный: {self.__model.get_answer()}")

