class Note:
    def __init__(self, text, date):
        self.__text = text
        self.__date = date

    def get_text(self):
        return self.__text

    def get_date(self):
        return self.__date

    def __str__(self):
        return f'{self.__text} {self.__date.toString("dd.MM.yyyy")}'
