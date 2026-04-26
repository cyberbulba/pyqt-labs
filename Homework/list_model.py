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
