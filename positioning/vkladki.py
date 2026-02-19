import sys

from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Времена года")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.6)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Вкладка 1")
        self.tabs.addTab(self.tab2, "Вкладка 2")
        self.tabs.addTab(self.tab3, "Вкладка 3")

        self.tabs.setFixedSize(self.height, self.height)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        layout = QGridLayout(self.tab1)
        layout.addWidget(QLabel('First'), 0, 0)

        #
        # self.layout = QVBoxLayout(self.central_widget)
        #
        # label = QLabel()
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # выравниваем по центру
        # self.layout.addWidget(label)
        # label.setText("Выберите время года:")
        #
        # self.text_edit = QTextEdit()
        # self.layout.addWidget(self.text_edit)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
