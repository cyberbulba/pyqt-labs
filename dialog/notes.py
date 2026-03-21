import sys

from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit, QDialog, \
    QCheckBox, QDateTimeEdit
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDate
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot
from Note import Note


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
        self.beginRemoveRows(QModelIndex(), row, row)
        self.__note_list.pop(row)
        self.endRemoveRows()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            item = self.__note_list[index.row()]
            return f"{item}"
        return None

    def updateRow(self, row, new_data):
        if 0 <= row < len(self.__note_list):
            self.__note_list[row] = new_data
            index = self.index(row)
            self.dataChanged.emit(index, index, [Qt.DisplayRole])


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить заметку")

        layout = QVBoxLayout()

        self.setLayout(layout)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Новая заметка")
        layout.addWidget(self.lineEdit)

        self.dateTimeEdit = QDateTimeEdit(QDate.currentDate())

        self.dateTimeEdit.setDisplayFormat("yyyy.MM.dd")
        self.dateTimeEdit.setCalendarPopup(True)
        layout.addWidget(self.dateTimeEdit)

        self.button = QPushButton("ОК")
        layout.addWidget(self.button)

        self.button.clicked.connect(self.close_dialog)

    def get_note(self):
        text = self.lineEdit.text()
        date = self.dateTimeEdit.date()
        self.lineEdit.clear()

        return Note(text, date)

    def close_dialog(self):
        self.accept()


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

        self.view = QListView()
        self.view.setModel(self.model)
        self.layout.addWidget(self.view)

        self.dialog = MyDialog()
        # self.dialog.accepted.connect(self.handle_add)

        self.view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction = QAction("Добавить заметку", self.view)
        self.view.addAction(self.addAction)
        self.addAction.triggered.connect(self.handle_add)

        self.changeAction = QAction("Изменить заметку", self.view)
        self.view.addAction(self.changeAction)
        self.changeAction.triggered.connect(self.handle_change)

    def handle_add(self):
        self.dialog.exec()

        note = self.dialog.get_note()
        if note.get_text().strip():
            self.model.addRow(note)

    def handle_change(self):
        self.dialog.exec()

        index = self.view.currentIndex().row()
        note = self.dialog.get_note()
        self.model.updateRow(index, note)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
