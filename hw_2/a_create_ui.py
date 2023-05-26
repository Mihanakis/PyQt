from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()  # инициализация интерфейса

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        # Тексты
        labelLogin = QtWidgets.QLabel("Логин")
        labelRegistration = QtWidgets.QLabel("Регистрация")

        # Окна ввода
        self.lineEditLogin = QtWidgets.QLineEdit()
        self.lineEditLogin.setPlaceholderText("Введите логин")

        self.lineEditPassword = QtWidgets.QLineEdit()
        self.lineEditPassword.setPlaceholderText("Введите пароль")
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        # пробовал вариант с PasswordEchoOnEdit, но у меня стирается строка при попытке донабрать пароль

        # Кнопки
        self.pushButtonLogin = QtWidgets.QPushButton()
        self.pushButtonLogin.setText("Войти")

        self.pushButtonRegistration = QtWidgets.QPushButton()
        self.pushButtonRegistration.setText("Регистрация")

        # Горизонтальные поля
        layoutLogin = QtWidgets.QHBoxLayout()
        layoutLogin.addWidget(labelLogin)
        layoutLogin.addWidget(self.lineEditLogin)

        layoutPassword = QtWidgets.QHBoxLayout()
        layoutPassword.addWidget(labelRegistration)
        layoutPassword.addWidget(self.lineEditPassword)

        layoutButtons = QtWidgets.QHBoxLayout()
        layoutButtons.addWidget(self.pushButtonLogin)
        layoutButtons.addWidget(self.pushButtonRegistration)

        # Объединение полей в одно поле по вертикали
        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutLogin)
        layoutMain.addLayout(layoutPassword)
        layoutMain.addLayout(layoutButtons)

        # Вызов единого (вертикального) поля
        self.setLayout(layoutMain)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
