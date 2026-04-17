import sys

from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot

class ListModel(QAbstractListModel):
    def __init__(self):
        super(ListModel, self).__init__()
        self.__note_list = []

    def rowCount(self, parent=None):
        return len(self.__note_list)

    def addRow(self, row):
        self.beginInsertRows(QModelIndex(), len(self.__note_list), len(self.__note_list))
        self.__note_list.append(row)
        self.endInsertRows()

    def removeRow(self, row):
        if 0 <= row < len(self.__note_list):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.__note_list.pop(row)
            self.endRemoveRows()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            item = self.__note_list[index.row()]
            return f"{item}"
        return None


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Заметки")
        self.model = ListModel()

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # узнаём размеры экрана и устанавливаем окно

        self.height = int(screen_geometry.height() * 0.5)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())  # перемещаем окно в центр
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        view = QListView()
        view.setModel(self.model)
        self.layout.addWidget(view)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Новая заметка")
        self.layout.addWidget(self.lineEdit)

        button = QPushButton("Ввести заметку")
        self.layout.addWidget(button)

        button.clicked.connect(self.handle_button)
        view.clicked.connect(self.click_on_note)

    @Slot()
    def handle_button(self):
        text = self.lineEdit.text()
        if text.strip() and any(i.isprintable() for i in text):
            self.model.addRow(text)
            self.lineEdit.clear()

    @Slot()
    def click_on_note(self, modelIndex):
        self.model.removeRow(modelIndex.row())