from PySide6.QtCore import QAbstractItemModel
from list_model import ListModel
from ExtraQuestionModel import QuestionModel


class MyModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.__num_lvl_1 = 0
        self.__num_lvl_2 = 0

        self.model = ListModel()
        self.question_model = QuestionModel()

    def add_info(self, level, info):
        """добавление информации о прохождении теста в wizard (1 или 2 уровня) в listModel"""
        if level == 1:
            self.__num_lvl_1 += 1
        elif level == 2:
            self.__num_lvl_2 += 1
        num = self.__num_lvl_1 if level == 1 else self.__num_lvl_2

        self.model.addRow(
            f'Тест lvl {level} № {num}: {info[0]} из {info[0] + info[1]} правильных ответов ({round(info[0] / (info[0] + info[1]) * 100, 2)}%), '
            f'ошибок в сложении: {info[2]}, в вычитании: {info[3]}, в умножении: {info[4]},'
            f'в делении: {info[5]}')

    def add_example_info(self, info):
        """добавление информации о решении примера с несколькими действиями (в dialog) в listModel"""
        self.model.addRow(f"Вы решили {'правильно' if info[0] == 1 else 'неправильно'} пример {info[1]}")

    def set_plus(self):
        """метод для генерации нового примера со знаком + в question_model"""
        self.question_model.generate_new_question("+")

    def set_minus(self):
        """метод для генерации нового примера со знаком - в question_model"""
        self.question_model.generate_new_question("-")

    def set_mult(self):
        """метод для генерации нового примера со знаком * в question_model"""
        self.question_model.generate_new_question("*")

    def set_div(self):
        """метод для генерации нового примера со знаком / в question_model"""
        self.question_model.generate_new_question("/")
