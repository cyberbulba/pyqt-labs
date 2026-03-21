class Note:
    def __init__(self, text, date):
        self.text = text
        self.date = date

    def get_text(self):
        return self.text

    def get_date(self):
        return self.date

    def __str__(self):
        return f'{self.text} {self.date.toString("dd.MM.yyyy")}'
