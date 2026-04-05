import sys

from PyQt6.QtCore import QVariant
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit, QCheckBox, \
    QDialog
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
        if not index.isValid():
            return None

        if role == Qt.DecorationRole:
            item = self.__note_list[index.row()]
            return item.scaled(200, 200)

        return None


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Список картинок")
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

        button = QPushButton("Выбрать картинку")
        self.layout.addWidget(button)

        self.dialog = QFileDialog()

        button.clicked.connect(self.get_file_path)

    @Slot()
    def get_file_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.model.addRow(QPixmap(file_path))


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
