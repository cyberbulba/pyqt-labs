import sys

from Book import Book
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QScrollArea


class MyWindow(QWidget):
    def __init__(self, books):
        super().__init__()
        self.books = books
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Список книг")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        height = int(screen_geometry.height() * 0.7)
        width = int(screen_geometry.width() * 0.8)
        self.setFixedSize(width, height)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        cont = QWidget()
        cont_layout = QVBoxLayout(cont)

        self.layout = QVBoxLayout(self)

        for book in self.books:
            self.create_text_label(book, cont_layout)

        scroll.setWidget(cont)
        self.layout.addWidget(scroll)

    def create_text_label(self, book):
        label = QLabel()
        label.setWordWrap(True)  # на каждую книгу 2 label: с текстом и картинкой
        label.setText(book.print_book())
        font = QFont("Times New Roman", 14)
        font.setItalic(True)
        label.setFont(font)
        label.setMargin(15)
        self.layout.addWidget(label)

        pix_label = QLabel()
        try:
            pixmap = QPixmap(book.get_file())
        except FileNotFoundError:
            print(f"нет фото{book.print_book()} ")
            exit(1)

        pixmap = pixmap.scaledToHeight(300)
        pix_label.setPixmap(pixmap)
        self.layout.addWidget(pix_label)


def main():
    books = ([Book("Тарас Бульба", "Гоголь", 300, "Books/bulba.jpg") for _ in range(20)] +
             [Book("Капитанская дочка", "Пушкин", 130, "Books/capitan_daughter.jpg") for _ in range(20)])

    app = QApplication(sys.argv)
    window = MyWindow(books)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
