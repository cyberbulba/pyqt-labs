class Product:
    def __init__(self, name, number, weight):
        self.name = name
        self.number = number
        self.weight = weight

    def get_all_weights(self):
        return self.weight * self.number

