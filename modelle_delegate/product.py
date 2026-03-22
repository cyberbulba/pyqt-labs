class Product:
    def __init__(self, name, number, weight):
        self.__name = name
        self.__number = number
        self.__weight = weight

    def get_all_weights(self):
        return self.__weight * self.__number

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_weight(self):
        return self.__weight
