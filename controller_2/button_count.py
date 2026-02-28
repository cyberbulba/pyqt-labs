import sys
from PySide6.QtWidgets import QPushButton, QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Signal, Slot, QObject


# Класс модели
class CounterModel(QObject):
    count_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.count = 0

    def increment(self):
        self.count += 1
        self.count_changed.emit(self.count)

    def reset(self):
        self.count = 0
        self.count_changed.emit(self.count)


class CounterController(QObject):
    increment_requested = Signal()
    reset_requested = Signal()

    def __init__(self, model, view):
        super().__init__()

        self.view = view
        self.model = model

        self.increment_requested.connect(self.model.increment)
        self.reset_requested.connect(self.model.reset)

        self.model.count_changed.connect(self.view.update_display)

        self.view.increment_button.clicked.connect(self.on_increment_button_clicked)
        self.view.reset_button.clicked.connect(self.on_reset_button_clicked)

    def on_increment_button_clicked(self):
        self.increment_requested.emit()

    def on_reset_button_clicked(self):
        self.reset_requested.emit()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Создаем модель и контроллер

    def initUI(self):
        self.setWindowTitle("Счётчик")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.height = int(screen_geometry.height() * 0.3)

        self.central_widget = QWidget()
        self.central_widget.setFixedSize(self.height, self.height)
        self.setCentralWidget(self.central_widget)

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

        self.layout = QVBoxLayout(self.central_widget)

        self.model = CounterModel()

        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.label.setText(f'{self.model.count}')

        self.increment_button = QPushButton("Увеличить число")
        self.layout.addWidget(self.increment_button)

        self.reset_button = QPushButton("Обнулить счётчик")
        self.layout.addWidget(self.reset_button)

        self.controller = CounterController(self.model, self)

    @Slot(int)
    def update_display(self, count):
        """Обновляет отображение счётчика"""
        self.label.setText(f"{count}")


def main():
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
