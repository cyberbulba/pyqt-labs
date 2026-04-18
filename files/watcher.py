from PySide6.QtCore import QFileSystemWatcher, QDir, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication


class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.__infoLabel = QLabel()
        layout.addWidget(self.__infoLabel)
        self.setLayout(layout)
        watcher = QFileSystemWatcher()
        isSuccess = watcher.addPath(str(QDir.currentPath()))
        print(isSuccess)
        print(watcher.directories())
        watcher.directoryChanged.connect(self.dirChanging)
        
    @Slot()
    def dirChanging(self, path):
        self.__infoLabel.setText(QDir(path).entryList())

app = QApplication([])
window = Window()
window.show()
app.exec()
