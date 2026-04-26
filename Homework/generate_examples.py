import random


class RandomExample1:
    def __init__(self, action=None, sign=1):
        self.__a = random.randint(-100, -1)

        if sign == 1:
            self.__b = random.randint(0, 100)
        else:
            self.__b = random.randint(-100, -1)

        if action is None:
            self.__action = random.choice(["+", "-", "*", "/"])
        else:
            self.__action = action

        if self.__action == "/" and self.__b == 0:
            self.__b = random.randint(1, 100)

    def get_result(self):
        """метод получает ответ на пример"""
        match self.__action:
            case "+":
                return self.__a + self.__b
            case "-":
                return self.__a - self.__b
            case "*":
                return self.__a * self.__b
            case "/":
                return round(self.__a / self.__b, 1)
        return None

    def get_a(self):
        """геттер для первого числа примера"""
        return self.__a

    def get_b(self):
        """геттер для второго числа примера"""
        return self.__b

    def get_action(self):
        """геттер для действия примера"""
        return self.__action

    def get_without_answer(self):
        """метод для получения примера без ответа"""
        return f'{self.get_a()} {self.get_action()} {self.get_b()} = ?'
