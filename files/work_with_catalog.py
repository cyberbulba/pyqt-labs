import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QFileSystemModel, QTreeView
from PySide6.QtWidgets import QPushButton, QButtonGroup, QRadioButton, QTextEdit, QListView, QLineEdit, QCheckBox, \
    QDialog
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QFileInfo, QDir
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
        self.system_model = QFileSystemModel()

        current_dir = QDir.currentPath()
        self.system_model.setRootPath(current_dir)

        tree = QTreeView()
        self.layout.addWidget(tree)
        tree.setModel(self.system_model)

        tree.setRootIndex(self.system_model.index(current_dir))

        tree.setWindowTitle("Файловый менеджер")
        tree.resize(600, 400)





def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
