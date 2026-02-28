import sys
from PySide6.QtWidgets import QPushButton, QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Signal, Slot, QObject


class ButtonController(QObject):
    button_pressed = Signal()
    button_released = Signal()

    def __init__(self, label):
        super().__init__()
        self.label = label

        self.button_pressed.connect(self.handle_button_pressed)
        self.button_released.connect(self.handle_button_released)

    @Slot()
    def handle_button_pressed(self):
        self.label.setText("Нажата")

    @Slot()
    def handle_button_released(self):
        self.label.setText("Отпущена")

    # Методы для генерации сигналов через emit
    def on_button_pressed(self):
        self.button_pressed.emit()  # Отправка сигнала через emit

    def on_button_released(self):
        self.button_released.emit()  # Отправка сигнала через emit


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Кнопка")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.height = int(screen_geometry.height() * 0.2)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.label.setText("Не нажата")

        button = QPushButton("Нажми на меня!")
        self.layout.addWidget(button)

        self.controller = ButtonController(self.label)

        button.pressed.connect(self.controller.on_button_pressed)
        button.released.connect(self.controller.on_button_released)


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()