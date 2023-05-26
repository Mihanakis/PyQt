from PySide6 import QtWidgets, QtCore
from picture import picture
from faker import Faker
fake = Faker('ru')


class WordBox(QtWidgets.QWidget):
    """
    Генератор одинаковых ячеек поля QLabel, с заранее заданными параметрами.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.wordBox = QtWidgets.QLabel()
        self.wordBox.setMinimumSize(40, 40)
        self.wordBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.wordBox.setEnabled(False)

        font = self.font()
        font.setPointSize(20)
        self.wordBox.setFont(font)
        self.wordBox.setText("*")


class HangmanGame(QtWidgets.QWidget):
    """Игра Виселица, логика и оформление"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()

        self.flag = False

    def initUi(self) -> None:
        """
        Метод создания окна из класса QtWidgets
        :return: None
        """
        self.setWindowTitle(f"HangmanGame - Mihanakis edition")
        self.setMinimumSize(500, 400)

        self.pushButtonStart = QtWidgets.QPushButton("Начать игру / Обновить слово")

        # answer layout -----------------------------------------------------------------------------------------------
        self.labelAnswer = QtWidgets.QLabel("Введите букву:")

        self.lineEditAnswer = QtWidgets.QLineEdit()
        self.lineEditAnswer.setPlaceholderText("Введите букву")
        self.lineEditAnswer.setEnabled(False)

        answerLayout = QtWidgets.QHBoxLayout()
        answerLayout.addWidget(self.labelAnswer)
        answerLayout.addWidget(self.lineEditAnswer)

        self.pushButtonAnswer = QtWidgets.QPushButton("Ответить")
        self.pushButtonAnswer.setEnabled(False)

        # layout plain text -------------------------------------------------------------------------------------------
        self.plainTextEditResult = QtWidgets.QPlainTextEdit()
        self.plainTextEditResult.appendPlainText("Добро пожаловать в игру Виселица!")
        self.plainTextEditResult.setEnabled(False)

        self.plainTextEditPicture = QtWidgets.QPlainTextEdit()
        self.plainTextEditPicture.setMinimumSize(90, 180)
        self.plainTextEditPicture.setMaximumSize(90, 180)
        self.plainTextEditPicture.setEnabled(False)

        plainTextLayout = QtWidgets.QHBoxLayout()
        plainTextLayout.addWidget(self.plainTextEditResult)
        plainTextLayout.addWidget(self.plainTextEditPicture)

        # Главный layout ----------------------------------------------------------------------------------------------
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.pushButtonStart)
        self.mainLayout.addLayout(answerLayout)
        self.mainLayout.addWidget(self.pushButtonAnswer)
        self.mainLayout.addLayout(plainTextLayout)

        self.setLayout(self.mainLayout)

    def initWord(self) -> None:
        """
        Метод инициализации загадываемого слова из модуля Faker.
        Не добавляет слово пока его длина меньше 8.
        :return: None
        """
        while True:
            str_ = fake.word()
            if len(str_) >= 8:
                print(str_)
                self.word = str_
                return

    def initSignals(self) -> None:
        """
        Метод передачи сигнала при нажатии кнопки.
        :return: None
        """
        self.pushButtonStart.clicked.connect(self.initField)
        self.pushButtonAnswer.clicked.connect(self.getWord)

    def initField(self):
        """
        Метод инициализации поля для игры.
        :return: None
        """
        if self.flag:
            self.wordGroupBox.deleteLater()
        self.wordGroupBox = QtWidgets.QGroupBox()
        self.wordGroupBox.setMinimumHeight(50)

        self.counter = 6
        self.initWord()
        self.answer = ["" for n in range(len(self.word))]

        self.lineEditAnswer.setEnabled(True)
        self.pushButtonAnswer.setEnabled(True)
        self.plainTextEditResult.setPlainText(f"Добро пожаловать в игру Виселица!")
        self.plainTextEditPicture.setPlainText("")
        self.fieldLayout = QtWidgets.QHBoxLayout()

        self.boxList = []
        for box in range(len(self.word)):
            wordBox = WordBox().wordBox
            self.fieldLayout.addWidget(wordBox)
            self.boxList.append(wordBox)
        self.wordGroupBox.setLayout(self.fieldLayout)
        self.mainLayout.addWidget(self.wordGroupBox)

        self.flag = True

    def validateEnterLetter(self, val) -> None:
        """
        Метод проверки вводимой пользователем буквы.
        :param val: Вводимая пользователем буква.
        :return: None
        """
        if val == '':
            self.plainTextEditResult.appendPlainText(f"Вы ничего не ввели, попробуйте снова.")
            return False
        if not val.isalpha():
            self.plainTextEditResult.appendPlainText(f"Вы ввели '{val}' - это не буква, попробуйте снова.")
            return False
        if len(val) > 1:
            self.plainTextEditResult.appendPlainText(f"Вы ввели больше одной буквы, попробуйте снова.")
            return False
        if val.lower() not in list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя'):
            self.plainTextEditResult.appendPlainText(f"Вы ввели букву не на русском языке. Смените раскладку.")
            return False
        return True

    def getWord(self) -> None:
        """
        Метод обработки вводимой буквы, добавления её на поле, счётчик оставшихся попыток.
        Также проверяет на победу или поражение.
        :return:
        """
        word = list(self.word)
        letter = self.lineEditAnswer.text().lower()
        if self.validateEnterLetter(letter):
            if letter in word:
                self.plainTextEditResult.appendPlainText(f"Вы выбрали букву '{letter.upper()}', она есть в этом слове.")
                for idx, val in enumerate(word):
                    if word[idx] == letter:
                        self.boxList[idx].setText(letter.upper())
                        self.answer[idx] = letter
            else:
                self.plainTextEditResult.appendPlainText(f"Вы выбрали букву '{letter.upper()}', её нет в этом слове.")
                self.counter -= 1
                self.plainTextEditResult.appendPlainText(f"Осталось попыток: {self.counter}.")
                self.plainTextEditPicture.setPlainText(picture[6 - self.counter])
            if self.answer == word:
                self.plainTextEditResult.appendPlainText(f"Вы угадали! Слово: {''.join(word).upper()}.")
            if self.counter == 0:
                self.lineEditAnswer.setEnabled(False)
                self.pushButtonAnswer.setEnabled(False)
                for idx, val in enumerate(word):
                    self.boxList[idx].setText(val.upper())
                self.plainTextEditResult.appendPlainText(f"Вы проиграли! Загаданное слово: {''.join(word).upper()}.")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = HangmanGame()
    window.show()

    app.exec()
