from PySide6.QtCore import QAbstractItemModel, Signal

from generate_examples import RandomExample1


class QuestionModel(QAbstractItemModel):
    exampleChanged = Signal()

    def __init__(self):
        super().__init__()
        self.__example = None

    def generate_new_question(self, action):
        """метод, который создаёт новый рандомный пример"""
        self.__example = RandomExample1(action, 0)
        self.exampleChanged.emit()

    def get_example(self):
        """метод, возвращающий текст примера (без ответа)"""
        if self.__example is not None:
            return self.__example.get_without_answer()
        return None

    def get_answer(self):
        """метод, возвращающий ответ на пример"""
        if self.__example is not None:
            return self.__example.get_result()
        return None
