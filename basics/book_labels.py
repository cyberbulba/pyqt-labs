import sys

from Book import Book
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QScrollArea


class MyWindow(QWidget):
    def __init__(self, books):
        super().__init__()
        self.books = books
        self.initUI()

    def initUI(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        cont = QWidget()
        cont_layout = QVBoxLayout(cont)

        self.height = screen_geometry.height()
        self.width = screen_geometry.width()
        layout = QVBoxLayout(self)

        self.setFixedSize(self.width, self.height)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

        for book in self.books:
            self.create_text_label(book.print_book(), cont_layout)

        scroll.setWidget(cont)
        layout.addWidget(scroll)

    def create_text_label(self, info, layout):
        label = QLabel()
        label.setWordWrap(True)
        label.setText(info)
        label.resize(self.height, self.height // 3)
        font = QFont("Times New Roman", 14)
        font.setItalic(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMargin(15)
        layout.addWidget(label)


def main():
    books = [Book("Петров", "Информатика", 260, "1") for i in range (20)]
    app = QApplication(sys.argv)
    window = MyWindow(books)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()