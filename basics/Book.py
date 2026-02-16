class Book():
    def __init__(self, name, author, pages, file):
        self.name = name
        self.author = author
        self.pages = pages
        self.file = file

    def print_book(self):
        return (f'Имя: {self.name}; Автор: {self.author}; Количество страниц: {self.pages}; '
                f'Ссылка на файл с обложкой: {self.file}')

    def get_file(self):
        return self.file

