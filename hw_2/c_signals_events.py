"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

from PySide6 import QtWidgets, QtCore, QtGui
from time import ctime


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSigngls()

    def initUi(self) -> None:
        """
        Инициализация Ui
        :return: None
        """
        self.setWindowTitle("Запуск ядерных ракет")

        # Кнопки панели навигации ------------------------------------------------------------------------
        self.moveLeftUpPushButton = QtWidgets.QPushButton("Лево-Верх")
        self.moveRightUpPushButton = QtWidgets.QPushButton("Право-Вверх")
        self.moveCenterPushButton = QtWidgets.QPushButton("Центр")
        self.moveLeftDownPushButton = QtWidgets.QPushButton("Лево-Низ")
        self.moveRightDownPushButton = QtWidgets.QPushButton("Право-Низ")

        layoutUpMoveButtons = QtWidgets.QHBoxLayout()
        layoutUpMoveButtons.addWidget(self.moveLeftUpPushButton)
        layoutUpMoveButtons.addWidget(self.moveRightUpPushButton)

        layoutCenterMoveButton = QtWidgets.QHBoxLayout()
        layoutCenterMoveButton.addWidget(self.moveCenterPushButton)

        layoutDownMoveButtons = QtWidgets.QHBoxLayout()
        layoutDownMoveButtons.addWidget(self.moveLeftDownPushButton)
        layoutDownMoveButtons.addWidget(self.moveRightDownPushButton)

        layoutMoveButtons = QtWidgets.QVBoxLayout()
        layoutMoveButtons.addLayout(layoutUpMoveButtons)
        layoutMoveButtons.addLayout(layoutCenterMoveButton)
        layoutMoveButtons.addLayout(layoutDownMoveButtons)

        self.groupBoxMoveButtons = QtWidgets.QGroupBox("Навигация")
        self.groupBoxMoveButtons.setLayout(layoutMoveButtons)

        # Строка SpeanBox --------------------------------------------------------------------------------
        self.spinBoxX = QtWidgets.QSpinBox()
        self.spinBoxX.setPrefix("x=")
        self.spinBoxX.setMaximum(500)

        self.spinBoxY = QtWidgets.QSpinBox()
        self.spinBoxY.setPrefix("y=")
        self.spinBoxY.setMaximum(500)

        layoutSpinBox = QtWidgets.QHBoxLayout()
        layoutSpinBox.addWidget(self.spinBoxX)
        layoutSpinBox.addWidget(self.spinBoxY)

        self.groupBoxSpinBox = QtWidgets.QGroupBox("Координаты")
        self.groupBoxSpinBox.setLayout(layoutSpinBox)

        # Строка изменения положения окна ----------------------------------------------------------------
        self.horizontalParamLineEdit = QtWidgets.QLineEdit()
        self.horizontalParamLineEdit.setPlaceholderText(f"Горизонталь")
        self.verticalSParamLineEdit = QtWidgets.QLineEdit()
        self.verticalSParamLineEdit.setPlaceholderText(f"Вертикаль")

        self.pushButtonSizeChange = QtWidgets.QPushButton("Передвинь меня!")

        layoutMoveWindow = QtWidgets.QHBoxLayout()
        layoutMoveWindow.addWidget(self.horizontalParamLineEdit)
        layoutMoveWindow.addWidget(self.verticalSParamLineEdit)
        layoutMoveWindow.addWidget(self.pushButtonSizeChange)

        self.groupBoxMoveWindow = QtWidgets.QGroupBox("Перемещение окна")
        self.groupBoxMoveWindow.setLayout(layoutMoveWindow)

        # Поле получения параметров----------------------------------------------------------------------
        self.pushButtonGetParameters = QtWidgets.QPushButton("Получить данные окна")
        self.pushButtonClear = QtWidgets.QPushButton("Очистить")

        layoutButtonsGetParameters = QtWidgets.QVBoxLayout()
        layoutButtonsGetParameters.addWidget(self.pushButtonGetParameters)
        layoutButtonsGetParameters.addWidget(self.pushButtonClear)

        self.plainTextEditGetParameters = QtWidgets.QPlainTextEdit()
        self.plainTextEditGetParameters.setPlaceholderText("Здесь могла быть ваша реклама.")

        layoutGetParameters = QtWidgets.QHBoxLayout()
        layoutGetParameters.addWidget(self.plainTextEditGetParameters)
        layoutGetParameters.addLayout(layoutButtonsGetParameters)

        self.groupBoxGetParameters = QtWidgets.QGroupBox("Статистика")
        self.groupBoxGetParameters.setLayout(layoutGetParameters)

        # Добавление виджета поля перемещения -----------------------------------------------------------
        self.groupBoxField = QtWidgets.QGroupBox("Поле")
        self.groupBoxField.setMaximumSize(500, 550)
        self.groupBoxField.setMinimumSize(500, 550)

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.textEdit.setEnabled(False)

        self.frame = QtWidgets.QFrame(self.textEdit)
        self.frame.setGeometry(QtCore.QRect(0, 0, 500, 500))

        self.frame.setStyleSheet("background-color: gray;")

        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setText("")
        self.radioButton.setEnabled(False)
        self.radioButton.setStyleSheet("background-color: blue;")

        self.pushButtonField = QtWidgets.QPushButton("Получить данные точки на поле")

        layoutField = QtWidgets.QVBoxLayout()
        layoutField.addWidget(self.textEdit)
        layoutField.addWidget(self.pushButtonField)

        self.groupBoxField.setLayout(layoutField)

        # Главное поле ----------------------------------------------------------------------------------
        leftMainLayout = QtWidgets.QVBoxLayout()
        leftMainLayout.addWidget(self.groupBoxMoveButtons)
        leftMainLayout.addWidget(self.groupBoxSpinBox)
        leftMainLayout.addWidget(self.groupBoxMoveWindow)
        leftMainLayout.addWidget(self.groupBoxGetParameters)

        self.groupBoxLeftMainLayout = QtWidgets.QGroupBox("Панель управления")
        self.groupBoxLeftMainLayout.setLayout(leftMainLayout)
        self.groupBoxLeftMainLayout.setMaximumWidth(450)

        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(self.groupBoxLeftMainLayout)
        mainLayout.addWidget(self.groupBoxField)

        self.setLayout(mainLayout)
        self.setMinimumSize(1100, 500)

    def initSigngls(self) -> None:
        self.pushButtonSizeChange.clicked.connect(self.onPushButtonSizeChangeCliced)
        self.pushButtonGetParameters.clicked.connect(self.onPushButtonGetParametersCliced)
        self.pushButtonClear.clicked.connect(self.onPushButtonClear)

        self.spinBoxX.valueChanged.connect(self.moveRadioButtonBySpinBox)
        self.spinBoxY.valueChanged.connect(self.moveRadioButtonBySpinBox)

        self.moveLeftUpPushButton.clicked.connect(self.onMoveLeftUpPushButtonClicked)
        self.moveRightUpPushButton.clicked.connect(self.onMoveRightUpPushButtonClicked)
        self.moveCenterPushButton.clicked.connect(self.onMoveCenterPushButtonClicked)
        self.moveLeftDownPushButton.clicked.connect(self.onMoveLeftDownPushButtonClicked)
        self.moveRightDownPushButton.clicked.connect(self.onMoveRightDownPushButtonClicked)

        self.pushButtonField.clicked.connect(self.onPushButtonFieldClicked)


    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        print(f"Изменено положение: {event.oldPos().toTuple()} -> {event.pos().toTuple()}, Время: {ctime()}")

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        print(f"Изменён размер окна: {event.oldSize().toTuple()} -> {event.size().toTuple()}, Время: {ctime()}")

    def onPushButtonSizeChangeCliced(self) -> None:
        h = self.horizontalParamLineEdit.text()
        v = self.verticalSParamLineEdit.text()
        if h != "" and v != "":
            if h.isdigit() and v.isdigit():
                h, v = int(h), int(v)
                if (h, v) > self.screen().size().toTuple():
                    raise ValueError("Значения больше размера экрана")
                self.move(h, v)
            else:
                raise TypeError("Введите числа")

    def onPushButtonClear(self) -> None:
        self.plainTextEditGetParameters.setPlainText("")

    def onPushButtonGetParametersCliced(self) -> None:
        self.plainTextEditGetParameters.setPlainText(f"Количество экранов: {len(QtWidgets.QApplication.screens())}\n"
                                                     f"Активный экран: {self.screen().name()}\n"
                                                     f"Разрешение экрана: {self.screen().size().toTuple()}\n"
                                                     f"Разрешение окна: {self.size().toTuple()}\n"
                                                     f"Минимальные размеры окна: {self.minimumSize().toTuple()}\n"
                                                     f"Текущее положение окна: {self.pos().toTuple()}\n"
                                                     f"Координаты центра окна: {self.geometry().center().toTuple()}\n"
                                                     f"Статус окна: {self.window().windowState().name}\n\n"
                                                     f"Время запроса: {ctime()}")

    def onPushButtonFieldClicked(self) -> None:
        self.plainTextEditGetParameters.setPlainText(f"Положение точки: {self.radioButton.pos().toTuple()}\n"
                                                     f"Размер поля: {self.frame.size().toTuple()}\n"
                                                     f"Положение центра {self.frame.geometry().center().toTuple()}\n"
                                                     f"\nПопытка запуска ядерных ракет.\n"
                                                     f"Ничего не произошло.\n"
                                                     f"У нас нет ядерных ракет.\n"
                                                     f"\nВремя запроса: {ctime()}")

    def moveRadioButtonBySpinBox(self):
        self.radioButton.move(self.spinBoxX.value(), self.spinBoxY.value())

    def onLeftUpPushButtonClicked(self):
        self.radioButton.move(self.radioButton.pos().toTuple()[0] - 5, self.radioButton.pos().toTuple()[1] - 5)

    def onMoveLeftUpPushButtonClicked(self):
        if self.radioButton.pos().toTuple() > (0, 0):
            x, y = self.radioButton.pos().toTuple()[0] - 5, self.radioButton.pos().toTuple()[1] - 5
            self.radioButton.move(x, y)
            self.spinBoxX.setValue(x)
            self.spinBoxY.setValue(y)

    def onMoveRightUpPushButtonClicked(self):
        x, y = self.radioButton.pos().toTuple()[0] + 5, self.radioButton.pos().toTuple()[1] - 5
        self.radioButton.move(x, y)
        self.spinBoxX.setValue(x)
        self.spinBoxY.setValue(y)

    def onMoveCenterPushButtonClicked(self):
        x, y = self.frame.geometry().center().toTuple()
        self.radioButton.move(x, y)
        self.spinBoxX.setValue(x)
        self.spinBoxY.setValue(y)

    def onMoveLeftDownPushButtonClicked(self):
        x, y = self.radioButton.pos().toTuple()[0] - 5, self.radioButton.pos().toTuple()[1] + 5
        self.radioButton.move(x, y)
        self.spinBoxX.setValue(x)
        self.spinBoxY.setValue(y)

    def onMoveRightDownPushButtonClicked(self):
        x, y = self.radioButton.pos().toTuple()[0] + 5, self.radioButton.pos().toTuple()[1] + 5
        self.radioButton.move(x, y)
        self.spinBoxX.setValue(x)
        self.spinBoxY.setValue(y)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
