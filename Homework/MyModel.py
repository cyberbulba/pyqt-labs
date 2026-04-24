from PySide6.QtCore import QAbstractItemModel
from list_model import ListModel
from extra_question import QuestionModel


class MyModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.num_lvl_1 = 0
        self.num_lvl_2 = 0

        self.model = ListModel()
        self.question_model = QuestionModel()

    def add_info(self, level, info):
        if level == 1:
            self.num_lvl_1 += 1
        elif level == 2:
            self.num_lvl_2 += 1
        num = self.num_lvl_1 if level == 1 else self.num_lvl_2

        self.model.addRow(
            f'Тест lvl {level} № {num}: {info[0]} из {info[0] + info[1]} правильных ответов ({round(info[0] / (info[0] + info[1]) * 100, 2)}%), '
            f'ошибок в сложении: {info[2]}, в вычитании: {info[3]}, в умножении: {info[4]},'
            f'в делении: {info[5]}')

    def add_example_info(self, info):
        self.model.addRow(f"Вы решили {'правильно' if info[0] == 1 else 'неправильно'} пример {info[1]}")

    def set_plus(self):
        self.question_model.generate_new_question("+")

    def set_minus(self):
        self.question_model.generate_new_question("-")

    def set_mult(self):
        self.question_model.generate_new_question("*")

    def set_div(self):
        self.question_model.generate_new_question("/")
