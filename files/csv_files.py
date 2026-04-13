import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit, QCheckBox, \
    QDialog
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QFileInfo
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Slot


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Выбор csv файла")

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

        button = QPushButton("Выбрать csv")
        self.layout.addWidget(button)

        self.file = ""

        self.dialog = QFileDialog()

        button.clicked.connect(self.get_file_info)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout.addWidget(self.textEdit)

    @Slot()
    def get_file_info(self):
        s = ''
        self.file, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "CSV files (*.csv)")
        if self.file:
            info = QFileInfo(self.file)
            s += f'Абсолютный путь: {info.absoluteFilePath()}\n'
            s += f'Базовое имя: {info.baseName()}\n'
            s += f'Можно читать: {info.isReadable()}\n'
            s += f'Можно писать: {info.isWritable()}\n'
            s += f'Исполняемый: {info.isExecutable()}\n'

            format = "dd.MM.yyyy HH:mm"

            s += f'Создан: {info.birthTime().toString(format)}\n'
            s += f'Последний раз изменён: {info.lastModified().toString(format)}\n'

            self.textEdit.setText(s)


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
