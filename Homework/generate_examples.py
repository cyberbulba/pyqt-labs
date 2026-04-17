import random


class RandomExample1:
    def __init__(self, action=None):
        self.__a = random.randint(-100, -1)
        self.__b = random.randint(-100, -1)
        if action is None:
            self.__action = random.choice(["+", "-", "*", "/"])
        else:
            self.__action = action

    def get_result(self):
        match self.__action:
            case "+":
                return self.__a + self.__b
            case "-":
                return self.__a - self.__b
            case "*":
                return self.__a * self.__b
            case "/":
                return self.__a // self.__b
        return None

    def get_a(self):
        return self.__a

    def get_b(self):
        return self.__b

    def get_action(self):
        return self.__action

    def get_without_answer(self):
        return f'{self.get_a()} {self.get_action()} {self.get_b()} = ?'

    def __str__(self):
        return f'{self.get_a()} {self.get_action()} {self.get_b()} = {self.get_result()}'
