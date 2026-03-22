import sys

from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit, QDialog, \
    QCheckBox, QDateTimeEdit
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDate
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
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

    def get_note(self, index):
        if index.isValid():
            return self.__note_list[index.row()]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.UserRole:
            self.__note_list[index.row()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Работа с заметкой")

        layout = QVBoxLayout()

        self.setLayout(layout)

        self.__lineEdit = QLineEdit()
        self.__lineEdit.setPlaceholderText("Новая заметка")
        layout.addWidget(self.__lineEdit)

        self.dateTimeEdit = QDateTimeEdit(QDate.currentDate())

        self.dateTimeEdit.setDisplayFormat("yyyy.MM.dd")
        self.dateTimeEdit.setCalendarPopup(True)
        layout.addWidget(self.dateTimeEdit)

        self.button = QPushButton("ОК")
        layout.addWidget(self.button)

        self.button.clicked.connect(self.close_dialog)

    def get_note(self):
        text = self.__lineEdit.text()
        date = self.dateTimeEdit.date()
        self.__lineEdit.clear()

        return Note(text, date)

    def close_dialog(self):
        self.accept()

    def set_text(self, text):
        self.__lineEdit.setText(text)


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
        self.selection_model = self.view.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)

        self.dialog = MyDialog()

        self.view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction = QAction("Добавить заметку", self.view)
        self.view.addAction(self.addAction)
        self.addAction.triggered.connect(self.handle_add)

        self.changeAction = QAction("Изменить заметку", self.view)
        self.view.addAction(self.changeAction)
        self.changeAction.triggered.connect(self.handle_change)
        self.changeAction.setEnabled(False)

        self.add_menu()

    def on_selection_changed(self):
        has_selection = self.selection_model.hasSelection()
        self.changeAction.setEnabled(has_selection)
        self.menuChange.setEnabled(has_selection)

    def handle_add(self):
        if self.dialog.exec() == QDialog.Accepted:
            note = self.dialog.get_note()
            if note.get_text().strip():
                self.model.addRow(note)

    def handle_change(self):
        index = self.view.currentIndex()

        if index.isValid():
            if self.view.selectionModel().hasSelection():
                current_text = self.model.get_note(index).get_text()
                self.dialog.set_text(current_text)
                if self.dialog.exec() == QDialog.Accepted:
                    note = self.dialog.get_note()
                    self.model.setData(index, note, Qt.UserRole)

    def add_menu(self):
        menuBar = self.menuBar()
        menuFile = menuBar.addMenu("Меню")
        menuCreate = menuFile.addAction("Создать новую заметку")
        self.menuChange = menuFile.addAction("Редактировать выбранную заметку")

        menuCreate.triggered.connect(self.handle_add)
        self.menuChange.triggered.connect(self.handle_change)
        self.menuChange.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
