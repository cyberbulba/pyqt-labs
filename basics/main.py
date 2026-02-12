import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

def create_window(screen):
    screen_geometry = screen.availableGeometry()

    # width = screen_geometry.width()
    height = screen_geometry.height()

    window = QMainWindow()
    window.resize(height, height)

    window_geometry = window.frameGeometry()
    window_geometry.moveCenter(screen_geometry.center())
    window.move(window_geometry.topLeft())

    return window

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()

window = create_window(screen)

window.show()
app.exec()
