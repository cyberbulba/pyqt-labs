from PySide6.QtWidgets import QGridLayout, QTextEdit, QListView, QTabWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow
from PySide6.QtCore import Slot

from Homework.extra_question import QuestionView
from wizard_1_lvl import MyWizard
from dialog import MyDialog
from MyModel import MyModel
from extra_question import QuestionView


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Обучение решению примеров с отрицательными числами")
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.height = int(screen_geometry.height())
        self.width = int(screen_geometry.width())

        self.central_widget = QTabWidget()
        self.central_widget.setMinimumSize(self.width, self.height)
        self.setCentralWidget(self.central_widget)
        window_geometry = self.frameGeometry()

        self.move(window_geometry.topLeft())

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.central_widget.addTab(self.tab1, "Главная")
        self.central_widget.addTab(self.tab2, "Доп. отработка навыков")

        self.initMainTabUI()
        self.initExtraTabUI()

    def initMainTabUI(self):
        self.layout_1 = QGridLayout(self.tab1)
        self.main_model = MyModel()

        train_label = QLabel("Тренировка:")
        self.layout_1.addWidget(train_label, 0, 6)

        self.button_lvl_1 = QPushButton("Тест (lvl 1)")
        self.layout_1.addWidget(self.button_lvl_1, 1, 6)

        self.button_lvl_2 = QPushButton("Тест (lvl 2)")
        self.layout_1.addWidget(self.button_lvl_2, 2, 6)

        self.button_lvl_3 = QPushButton("Сложный пример (lvl 3)")
        self.layout_1.addWidget(self.button_lvl_3, 3, 6)

        question_label = QLabel("Справочные материалы по действиям с отрицательными числами")
        self.layout_1.addWidget(question_label, 0, 0, 1, 5)

        self.button_plus = QPushButton("+")
        self.layout_1.addWidget(self.button_plus, 1, 0)
        self.button_plus.clicked.connect(self.handle_plus)

        self.button_minus = QPushButton("-")
        self.layout_1.addWidget(self.button_minus, 1, 1)
        self.button_minus.clicked.connect(self.handle_minus)

        self.button_mult = QPushButton("*")
        self.layout_1.addWidget(self.button_mult, 1, 2)
        self.button_mult.clicked.connect(self.handle_mult)

        self.button_div = QPushButton("/")
        self.layout_1.addWidget(self.button_div, 1, 3)
        self.button_div.clicked.connect(self.handle_div)

        self.button_many_actions = QPushButton("Несколько действий")
        self.layout_1.addWidget(self.button_many_actions, 1, 4)
        self.button_many_actions.clicked.connect(self.many_actions_info)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout_1.addWidget(self.textEdit, 2, 0, 1, 5)

        view = QListView()
        view.setModel(self.main_model.model)
        self.layout_1.addWidget(view, 3, 0, 1, 5)

        self.wizard_lvl_1 = MyWizard(level=1)
        self.wizard_lvl_2 = MyWizard(level=2)

        self.button_lvl_1.clicked.connect(self.open_wizard_lvl_1)
        self.button_lvl_2.clicked.connect(self.open_wizard_lvl_2)

        self.wizard_lvl_1.accepted.connect(self.finish_wizard_lvl_1)
        self.wizard_lvl_2.accepted.connect(self.finish_wizard_lvl_2)

        self.dialog = MyDialog()
        self.button_lvl_3.clicked.connect(self.open_dialog)
        self.dialog.accepted.connect(self.finish_lvl_3)

    def initExtraTabUI(self):
        self.layout_2 = QGridLayout(self.tab2)

        self.test_question = QuestionView()
        self.test_question.setModel(self.main_model.question_model)
        self.layout_2.addWidget(self.test_question, 0, 1, 4, 1)

        self.button_plus = QPushButton("+")
        self.layout_2.addWidget(self.button_plus, 0, 0)
        self.button_plus.clicked.connect(self.set_plus_question)

        self.button_minus = QPushButton("-")
        self.layout_2.addWidget(self.button_minus, 1, 0)
        self.button_minus.clicked.connect(self.set_minus_question)

        self.button_mult = QPushButton("*")
        self.layout_2.addWidget(self.button_mult, 2, 0)
        self.button_mult.clicked.connect(self.set_mult_question)

        self.button_div = QPushButton("/")
        self.layout_2.addWidget(self.button_div, 3, 0)
        self.button_div.clicked.connect(self.set_div_question)

    @Slot()
    def set_plus_question(self):
        self.main_model.set_plus()

    @Slot()
    def set_minus_question(self):
        self.main_model.set_minus()

    @Slot()
    def set_mult_question(self):
        self.main_model.set_mult()

    @Slot()
    def set_div_question(self):
        self.main_model.set_div()

    @Slot()
    def open_wizard_lvl_1(self):
        self.wizard_lvl_1.exec()

    @Slot()
    def open_wizard_lvl_2(self):
        self.wizard_lvl_2.exec()

    @Slot()
    def open_dialog(self):
        self.dialog.exec()

    @Slot()
    def handle_plus(self):
        self.textEdit.setText("Рассмотрим сложение с отрицательным числом:\n "
                              "1. Если число, к которому прибавляем положительное, пример -3 + 5, \n"
                              "тогда чтобы получить ответ, необходимо вычесть из него отрицательное число, то есть 5 - 3 = 2\n"
                              "2. Если число, к которому прибавляем отрицательное, например -3 - 5, то необходимо сложить модули\n"
                              "этих чисел: 3 + 5 = 8 и заменить знак на противоположный, таким образом -3 - 5 = -8\n"
                              "3. Если число, к которому прибавляем является 0, например -3 + 0 то в ответ следует записать само отрицательное число: -3 + 0 = -3\n")

    @Slot()
    def handle_minus(self):
        self.textEdit.setText("Рассмотрим вычитание из отрицательного числа:\n "
                              "1. Если из отрицательного числа вычитаем положительное, пример -3 - 5, \n"
                              "тогда необходимо сложить модули чисел: 3 + 5 = 8 и поставить знак минус: -3 - 5 = -8\n"
                              "2. Если из числа вычитаем отрицательное, например -3 - (-5), то два минуса дают плюс, то\n"
                              "заменяем вычитание на сложение: -3 + 5 = 2\n"
                              "3. Если вычитаемое равно 0, например -3 - 0, то число не изменяется: -3 - 0 = -3\n")

    @Slot()
    def handle_mult(self):
        self.textEdit.setText("Рассмотрим умножение с отрицательным числом:\n "
                              "1. Если отрицательное число умножаем на отрицательное, пример -3 * (-5), \n"
                              "тогда минус на минус дает плюс. Перемножаем модули: 3 * 5 = 15, результат: 15\n"
                              "2. Если отрицательное число умножаем на положительное, например -3 * 5, то результат будет отрицательным: \n"
                              "3 * 5 = 15, и заменить знак на противоположный: -15\n"
                              "3. Если один из множителей равен 0, например -3 * 0, то произведение равно 0\n")

    @Slot()
    def handle_div(self):
        self.textEdit.setText("Рассмотрим деление с отрицательным числом:\n "
                              "1. Если отрицательное число делим на отрицательное, пример -10 / (-2), \n"
                              "тогда минус на минус дает плюс. Делим модули: 10 / 2 = 5, результат: 5\n"
                              "2. Если отрицательное число делим на положительное, например -10 / 2, то результат будет отрицательным: \n"
                              "10 / 2 = 5, и заменить знак на противоположный: -5\n"
                              "3. Если делимое равно 0, например 0 / (-5), то частное равно 0\n")

    @Slot()
    def many_actions_info(self):
        self.textEdit.setText(
            "Порядок выполнения действий в выражениях (тот же самый, если бы у нас были положительные числа):\n "
            "1. Первыми всегда вычисляются действия в скобках ( ), например в выражении (-10 - 4) * 2 \n"
            "сначала решаем скобку: -10 - 4 = -14, затем умножаем: -14 * 2 = -28\n"
            "2. Умножение и деление имеют одинаковый приоритет и выполняются строго слева направо, \n"
            "например -16 / 4 * 3. Делим -16 на 4, получаем -4, затем умножаем на 3: -4 * 3 = -12\n"
            "3. Сложение и вычитание выполняются в последнюю очередь, также слева направо, \n"
            "например -25 - 8 + 5. Сначала вычитаем: -25 - 8 = -33, затем прибавляем: -33 + 5 = -28\n"
            "4. Если в выражении есть отрицательные числа, их знаки учитываются на каждом шаге, \n"
            "например -7 + (-3) * (-4). Сначала умножение: -3 * (-4) = 12, затем сложение: -7 + 12 = 5\n")

    @Slot()
    def finish_wizard_lvl_1(self):
        self.main_model.add_info(1, self.wizard_lvl_1.get_statistic())
        self.wizard_lvl_1.reset_wizard()

    @Slot()
    def finish_wizard_lvl_2(self):
        self.main_model.add_info(2, self.wizard_lvl_2.get_statistic())
        self.wizard_lvl_2.reset_wizard()

    @Slot()
    def finish_lvl_3(self):
        info = self.dialog.get_result()
        self.main_model.add_example_info(info)

        self.dialog.reset()
