from PySide6 import QtWidgets, QtCore, QtGui
from random import randint


class NumBox(QtWidgets.QWidget):
    """
    Генератор одинаковых ячеек поля QLabel, с заранее заданными параметрами.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.numBox = QtWidgets.QLabel()
        self.numBox.setMinimumSize(60, 60)
        self.numBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.numBox.setEnabled(False)

        font = self.font()
        font.setPointSize(32)
        self.numBox.setFont(font)
        self.numBox.setText("")


class LineEditBox(QtWidgets.QWidget):
    """
    Генератор одинаковых ячеек вывода результатов QLineEdit, с заранее заданными параметрами.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.lineEditBox = QtWidgets.QLineEdit()
        self.lineEditBox.setMaximumSize(120, 38)
        self.lineEditBox.setEnabled(False)

        font = self.font()
        font.setPointSize(18)
        self.lineEditBox.setFont(font)


class Game2048(QtWidgets.QWidget):
    """Игра 2048, логика и оформление"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.flag = False  # флаг проверки который при срабатывании не даёт перехватывать нажатия
        self.settings = QtCore.QSettings('Data')  # сохранённые результаты после закрытия окна

        self.bestScore = 0  # лучший счёт

        self.initUi()
        self.initSignals()

        self.color_db = {
            '0': 'white',
            '2': '#eee6db',
            '4': '#ece0c8',
            '8': '#efb27c',
            '16': '#f39768',
            '32': '#f37d63',
            '64': '#f46042',
            '128': '#eacf76',
            '256': '#edcb67',
            '512': '#ecc85a',
            '1024': '#e7c257',
            '2048': '#e8be4e'}

        self.initFieldList()    # инициализация поля
        self.getScore()         # инициализация атрибута self.score и подсчёт первого значение счёта

        self.cheat = []         # атрибут хранения чит-кода

    def initUi(self) -> None:
        """
        Метод создания окна из класса QtWidgets
        :return: None
        """
        self.setWindowTitle(f"Game2048 - Mihanakis edition")
        self.setMaximumSize(500, 610)
        self.setMinimumSize(500, 610)

        # layout кнопки сброса и вывода результатов -------------------------------------------------------------------
        self.pushButtonReset = QtWidgets.QPushButton("New Game")
        self.pushButtonReset.setMinimumSize(130, 60)
        font = self.font()
        font.setPointSize(13)
        self.pushButtonReset.setFont(font)

        self.currentScoreLabel = QtWidgets.QLabel("Current:")
        self.currentScoreLineEdit = LineEditBox().lineEditBox

        self.bestScoreLabel = QtWidgets.QLabel("Best:")
        self.bestScoreLineEdit = LineEditBox().lineEditBox

        if self.settings:       # восстановление значений, если окно было закрыто
            self.bestScore = self.settings.value("Number", 0)
            self.bestScoreLineEdit.setText(str(self.bestScore))

        scoresLayout = QtWidgets.QHBoxLayout()
        scoresLayout.addWidget(self.pushButtonReset)
        scoresLayout.addWidget(self.currentScoreLabel)
        scoresLayout.addWidget(self.currentScoreLineEdit)
        scoresLayout.addWidget(self.bestScoreLabel)
        scoresLayout.addWidget(self.bestScoreLineEdit)

        self.scoreGroupBox = QtWidgets.QGroupBox("Scores")
        self.scoreGroupBox.setLayout(scoresLayout)
        self.scoreGroupBox.setMaximumSize(400, 65)

        scoresAndResetLayout = QtWidgets.QHBoxLayout()
        scoresAndResetLayout.addWidget(self.pushButtonReset)
        scoresAndResetLayout.addWidget(self.scoreGroupBox)

        # layout-ы первой, второй, третьей и четвертой горизонталей ---------------------------------------------------
        self.box11, self.box12, self.box13, self.box14 = \
            NumBox().numBox, NumBox().numBox, NumBox().numBox, NumBox().numBox

        firstHorizontalLayout = QtWidgets.QHBoxLayout()
        firstHorizontalLayout.addWidget(self.box11)
        firstHorizontalLayout.addWidget(self.box12)
        firstHorizontalLayout.addWidget(self.box13)
        firstHorizontalLayout.addWidget(self.box14)

        self.box21, self.box22, self.box23, self.box24 = \
            NumBox().numBox, NumBox().numBox, NumBox().numBox, NumBox().numBox

        secondHorizontalLayout = QtWidgets.QHBoxLayout()
        secondHorizontalLayout.addWidget(self.box21)
        secondHorizontalLayout.addWidget(self.box22)
        secondHorizontalLayout.addWidget(self.box23)
        secondHorizontalLayout.addWidget(self.box24)

        self.box31, self.box32, self.box33, self.box34 = \
            NumBox().numBox, NumBox().numBox, NumBox().numBox, NumBox().numBox

        thirdHorizontalLayout = QtWidgets.QHBoxLayout()
        thirdHorizontalLayout.addWidget(self.box31)
        thirdHorizontalLayout.addWidget(self.box32)
        thirdHorizontalLayout.addWidget(self.box33)
        thirdHorizontalLayout.addWidget(self.box34)

        self.box41, self.box42, self.box43, self.box44 = \
            NumBox().numBox, NumBox().numBox, NumBox().numBox, NumBox().numBox

        fourthHorizontalLayout = QtWidgets.QHBoxLayout()
        fourthHorizontalLayout.addWidget(self.box41)
        fourthHorizontalLayout.addWidget(self.box42)
        fourthHorizontalLayout.addWidget(self.box43)
        fourthHorizontalLayout.addWidget(self.box44)

        # layout справки ---------------------------------------------------------------------------------------------
        self.helpLineEdit = QtWidgets.QLabel(f"Keyboard: W-up, A-left, S-down, D-right.")
        self.helpLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.helpLineEdit.setMaximumHeight(16)
        self.helpLineEdit.setEnabled(False)

        # Главный layout ----------------------------------------------------------------------------------------------
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(scoresAndResetLayout)
        mainLayout.addLayout(firstHorizontalLayout)
        mainLayout.addLayout(secondHorizontalLayout)
        mainLayout.addLayout(thirdHorizontalLayout)
        mainLayout.addLayout(fourthHorizontalLayout)
        mainLayout.addWidget(self.helpLineEdit)

        self.setLayout(mainLayout)

        # все окна собраны в один список для удобства вызова
        self.boxList = [self.box11, self.box12, self.box13, self.box14, self.box21, self.box22, self.box23, self.box24,
                        self.box31, self.box32, self.box33, self.box34, self.box41, self.box42, self.box43, self.box44]

        # отслеживание нажатия кнопок управления игрой пользователем кнопкой интерфейса "New Game"
        self.pushButtonReset.installEventFilter(self)

    def initSignals(self) -> None:
        """
        Метод передачи сигнала при нажатии кнопки.
        :return: None
        """
        self.pushButtonReset.clicked.connect(self.clearField)

    def initFieldList(self) -> None:
        """
        Метод первой инициализиации пустого поля, добавляет значения "2" или "4" 2 раза в произвольные ячейки.
        :return: None
        """
        self.fieldList = []
        for i in range(16):
            self.fieldList.append(0)

        self.stepRandomAddNumOnField()
        self.stepRandomAddNumOnField()

    def clearField(self) -> None:
        """
        Метод для очистки поля и значения текущего счёта.
        :return: None
        """
        self.flag = False
        self.initFieldList()
        self.getScore()

    def setNumbersOnField(self) -> None:
        """
        Метод задающий в ячейки поля цифры из списка и соответствующий цвет фона.
        :return: None
        """
        for n in range(len(self.fieldList)):
            if self.fieldList[n] == 0:
                self.boxList[n].setText("")
            else:
                self.boxList[n].setText(str(self.fieldList[n]))

            if str(self.fieldList[n]).isdigit():
                self.boxList[n].setStyleSheet(f"background-color: {self.color_db[str(self.fieldList[n])]}")
            else:
                self.boxList[n].setStyleSheet(f"background-color: '{self.color_db['0']}'")
        self.getScore()

    def gameOverCheck(self) -> bool:
        """
        Метод проверки на поражение. Если поле заполнено - игра окончена.
        :return: bool: True - если игра закончена и False если можно продолжать.
        """
        counter = 0
        for n in self.fieldList:
            if n == 0:
                return False
            counter += 1
            if counter == len(self.fieldList):
                self.fieldList = ["", "", "", "", "G", "A", "M", "E", "O", "V", "E", "R", "", "", "", ""]
                self.setNumbersOnField()
                self.fieldList.clear()
                return True

    def isWinCheck(self) -> bool:
        """
        Метод проверки на победу, если достигнуто число 2048.
        :return: bool: True - если достигнута победа и False если нет.
        """
        for n in self.fieldList:
            if n == 2048:
                self.fieldList = ["", "", "", "", "Y", "O", "U", "", "", "W", "I", "N", "", "", "", ""]
                self.setNumbersOnField()
                self.fieldList.clear()
                return True
        return False

    def stepRandomAddNumOnField(self) -> None:
        """
        Метод добавления "2" или "4" (с 10% шансом) в произвольную свободную ячейку поля.
        :return: None
        """
        if not self.flag:
            val = 0
            while val != 1:
                index = randint(0, 15)
                if self.fieldList[index] == 0:
                    self.fieldList[index] = (4 if randint(1, 10) == 10 else 2)
                    val += 1
            self.setNumbersOnField()

    def editCheatCode(self) -> None:
        """
        Метод, который изменяет поле, убирая все значение менее 17.
        """
        cheatFieldList = []
        for n in self.fieldList:
            cheatFieldList.append(0 if n < 17 else n)
            if sum(cheatFieldList) > 0:
                self.fieldList = cheatFieldList
                self.setNumbersOnField()

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Метод перехватывающий нажатия необходимых кнопок для игры - "wasd" или "цфыв", а также кнопок для чит-кодов.
        В этом методе к кнопкам подключена логика движения чисел по полю.
        :param watched: QtCore.QObject
        :param event: QtCore.QEvent
        :return: bool
        """
        if watched == self.pushButtonReset and event.type() == QtCore.QEvent.Type.KeyPress:
            if not self.flag:
                if event.text().lower() in ['w', 'ц']:
                    self.upKeyPressed()
                if event.text().lower() in ['a', 'ф']:
                    self.leftKeyPressed()
                    self.cheat.append("a")
                    if self.cheat == ["m", "i", "h", "a"]:
                        self.fieldList = [512] + [0, 0] + [512] + [0 for n in range(8)] + [512] + [0, 0] + [512]
                        self.setNumbersOnField()
                    self.cheat.clear()
                if event.text().lower() in ['s', 'ы']:
                    self.downKeyPressed()
                if event.text().lower() in ['d', 'в']:
                    self.rightKeyPressed()
                    self.cheat.append("d")

                # проверка ввода чит-кода 1 - легкая победа
                if event.text().lower() in ['m', 'ь']:
                    self.cheat.append("m")
                if event.text().lower() in ['i', 'ш']:
                    self.cheat.append("i")
                if event.text().lower() in ['h', 'р']:
                    self.cheat.append("h")

                # проверка ввода чит-кода 2 - сброс лучшего результата
                if event.text().lower() in ['r', 'к']:
                    self.cheat.append("r")
                if event.text().lower() in ['o', 'щ']:
                    self.cheat.append("o")
                if event.text().lower() in ['p', 'з']:
                    self.cheat.append("p")
                    if self.cheat == ["d", "r", "o", "p"]:
                        self.bestScore = 0
                        self.getScore()

                # проверка ввода чит-кода 3 - убрать результаты меньше 17
                if event.text().lower() in ['e', 'у']:
                    self.cheat.append("e")
                if event.text().lower() in ['t', 'е']:
                    self.cheat.append("t")
                    if self.cheat == ["e", "d", "i", "t"]:
                        self.editCheatCode()

        return super(Game2048, self).eventFilter(watched, event)

    def tempFieldChecher(funk) -> callable:
        """
        Декоратор дополнительных функций при нажатии управляющих клавиш.

        Выполняет 2 задачи:
        1. Проверяет изменение положения чисел на поле в результате нажатия управляющих клавиш.
        Не добавляет новых элементов, если изменения положения не было и наоборот.
        2. Проводит проверку результатов нажатия - есть ли победа или проигрыш и изменяет значение флага self.flag.
        :return: callable - метод, который использует декоратор.
        """
        def wrapper(self):
            tempFieldList = self.fieldList.copy()
            funk(self)
            self.flag = self.isWinCheck()
            if tempFieldList != self.fieldList:
                self.stepRandomAddNumOnField()
            else:
                self.setNumbersOnField()
                self.flag = self.gameOverCheck()  # важен вызов этого метода именно в момент когда поле не изменилось
        return wrapper

    @tempFieldChecher
    def leftKeyPressed(self) -> None:
        """
        Метод перемещения цифр поля влево по строкам по нажатию кнопок "a" или "ф".
        Складывает при одинаковых значениях или перемещает если поле слева пустое.
        :return: None
        """
        for k in range(3):
            for m in range(0, 13, 4):
                for n in range(0 + m, 3 + m):
                    if self.fieldList[n] == self.fieldList[n + 1] or self.fieldList[n] == 0:
                        self.fieldList[n] += self.fieldList[n + 1]
                        self.fieldList[n + 1] = 0

    @tempFieldChecher
    def rightKeyPressed(self) -> None:
        """
        Метод перемещения цифр поля вправо по строкам по нажатию кнопок "d" или "а".
        Складывает при одинаковых значениях или перемещает если поле справа пустое.
        :return: None
        """
        for k in range(3):
            for m in range(0, 13, 4):
                for n in range(3 + m, 0 + m, -1):
                    if self.fieldList[n] == self.fieldList[n - 1] or self.fieldList[n] == 0:
                        self.fieldList[n] += self.fieldList[n - 1]
                        self.fieldList[n - 1] = 0

    @tempFieldChecher
    def upKeyPressed(self) -> None:
        """
        Метод перемещения цифр поля вверх по столбцам по нажатию кнопок "w" или "ц".
        Складывает при одинаковых значениях или перемещает если поле сверху пустое.
        :return: None
        """
        for k in range(3):
            for m in range(4):
                for n in range(0 + m, 9 + m, 4):
                    if self.fieldList[n] == self.fieldList[n + 4] or self.fieldList[n] == 0:
                        self.fieldList[n] += self.fieldList[n + 4]
                        self.fieldList[n + 4] = 0

    @tempFieldChecher
    def downKeyPressed(self) -> None:
        """
        Метод перемещения цифр поля вниз по столбцам по нажатию кнопок "s" или "ы".
        Складывает при одинаковых значениях или перемещает если поле внизу пустое.
        :return: None
        """
        for k in range(3):
            for m in range(4):
                for n in range(12 + m, 3 + m, -4):
                    if self.fieldList[n] == self.fieldList[n - 4] or self.fieldList[n] == 0:
                        self.fieldList[n] += self.fieldList[n - 4]
                        self.fieldList[n - 4] = 0

    def getScore(self) -> None:
        """
        Метод вызываемый при нажатии кнопок на которые настроены триггеры.

        Выполняет 3 задачи:
        1. Инициализирует атрибут self.score в классе Game2024;
        2. Рассчитывает по формуле текущий счёт и записывает результат вычислений в окно текущего счёта;
        4. Сравнивает текущий счёт с лучшим и если лучший меньше - переписывает его и изменяет значение в окне.
        :return: None
        """
        self.score = []
        for n in self.fieldList:
            if isinstance(n, int):
                if n > 2:
                    counter = 0
                    while n != 2:
                        counter += 1
                        self.score.append(int(n) * counter)
                        n = n / 2

        self.currentScoreLineEdit.setText(str(sum(self.score)))
        if sum(self.score) >= int(self.bestScore):
            self.bestScore = sum(self.score)
            self.bestScoreLineEdit.setText(str(self.bestScore))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Метод сохраняющий лучший счёт при закрытии окна.
        :param event: QtGui.QCloseEvent
        :return: None
        """
        self.settings.setValue("Number", self.bestScoreLineEdit.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Game2048()
    window.show()

    app.exec()