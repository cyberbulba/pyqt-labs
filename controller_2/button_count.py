import sys
from PySide6.QtWidgets import QPushButton, QApplication, QLabel, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtCore import Signal, Slot, QObject


# Класс модели
class CounterModel(QObject):
    """Модель, хранящая данные счётчика и реализующая бизнес-логику"""
    # Сигнал для уведомления о изменении значения счётчика
    count_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._count = 0

    @property
    def count(self):
        return self._count

    def increment(self):
        """Увеличить счётчик на 1"""
        self._count += 1
        self.count_changed.emit(self._count)

    def reset(self):
        """Сбросить счётчик в ноль"""
        self._count = 0
        self.count_changed.emit(self._count)


# Класс контроллера
class CounterController(QObject):
    """Контроллер, обрабатывающий пользовательские действия и управляющий моделью"""
    # Сигналы контроллера для обработки пользовательских действий
    increment_requested = Signal()
    reset_requested = Signal()

    def __init__(self, model, view):
        super().__init__()

        self.view = view
        self.model = model
        # Подключаем сигналы контроллера к методам модели
        self.increment_requested.connect(self.model.increment)
        self.reset_requested.connect(self.model.reset)

        # Подключаем сигналы модели к виду
        self.model.count_changed.connect(self.view.update_display)

        # Подключаем кнопки вида к контроллеру
        self.view.increment_button.clicked.connect(self.on_increment_button_clicked)
        self.view.reset_button.clicked.connect(self.on_reset_button_clicked)

    def on_increment_button_clicked(self):
        """Обработчик нажатия кнопки 'Увеличить' - генерирует сигнал через emit"""
        self.increment_requested.emit()

    def on_reset_button_clicked(self):
        """Обработчик нажатия кнопки 'Сбросить' - генерирует сигнал через emit"""
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

        # 1. Create model FIRST
        self.model = CounterModel()

        # 2. Create UI elements (label and buttons)
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.label.setText(f'{self.model.count}')  # Set initial value

        self.increment_button = QPushButton("Увеличить число")
        self.layout.addWidget(self.increment_button)

        self.reset_button = QPushButton("Обнулить счётчик")
        self.layout.addWidget(self.reset_button)

        # 3. Create controller LAST (after buttons exist)
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