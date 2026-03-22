import sys

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit, QTableView, \
    QSpinBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot

from modelle_delegate.product import Product


class TableModel(QAbstractTableModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.__note_list = self.__create_default_data()

    def __create_default_data(self):
        return [Product("Виноград", 2, 2),
                Product("Сливы", 2, 2),
                Product("Яблоки зелёные", 2, 2),
                Product("Бананы", 2, 2)]

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

    def rowCount(self, parent=None):
        return len(self.__note_list)

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            product = self.__note_list[index.row()]
            if index.column() == 0:
                return product.get_name()
            elif index.column() == 1:
                return product.get_number()
            elif index.column() == 2:
                return product.get_weight()
            else:
                return 0
        return None

    def headerData(self, col, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            headers = ["Название", "Количество, шт", "Масса, кг"]
            if col < len(headers):
                return headers[col]
        return None

    def get_all_weights_of_table(self):
        count = 0
        for item in self.__note_list:
            count += item.get_all_weights()
        return count


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Список продуктов")
        self.model = TableModel()

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

        view = QTableView()
        view.setModel(self.model)
        self.layout.addWidget(view)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Название продукта")
        self.layout.addWidget(self.lineEdit)

        self.layout.addWidget(QLabel("Выберите количество продукта:"))
        self.spinbox_num = QSpinBox()
        self.layout.addWidget(self.spinbox_num)

        self.layout.addWidget(QLabel("Выберите массу продукта:"))
        self.spinbox_weight = QSpinBox()
        self.spinbox_weight.setSuffix(' кг')
        self.layout.addWidget(self.spinbox_weight)

        button = QPushButton("Ввести заметку")
        self.layout.addWidget(button)

        self.cost_widget = QLabel(f"Итого: {self.model.get_all_weights_of_table()} кг")
        self.layout.addWidget(self.cost_widget)

        button.clicked.connect(self.handle_button)

    def handle_button(self):
        text = self.lineEdit.text()
        num = self.spinbox_num.value()
        weight = self.spinbox_weight.value()
        if text.strip() and num and weight:
            self.model.addRow(Product(text, num, weight))
            self.lineEdit.clear()
            self.spinbox_num.clear()
            self.spinbox_weight.clear()

            self.cost_widget.setText(f'Итого: {self.model.get_all_weights_of_table()} кг')


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
