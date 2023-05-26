"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)
Программа должна обладать следующим функционалом:
1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль
2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)
3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.
4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""
from PySide6 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings('Data')

        self.unitUi()
        self.initSignals()

    def unitUi(self) -> None:
        number = int(self.settings.value("Number", 0))
        measure = self.settings.value("CheckState", "")

        self.setWindowTitle("Декодер Тьюринга")

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(['oct', 'hex', 'bin', 'dec'])

        self.dial = QtWidgets.QDial()
        self.dial.installEventFilter(self)

        self.lcdNumber = QtWidgets.QLCDNumber()

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        if self.settings:
            self.comboBox.setCurrentText(measure)
            self.dial.setValue(number)
            self.slider.setValue(number)
            self.lcdNumber.display(self.transferVal(number))

        # Задание полей -------------------------------------------------------------
        layoutRight = QtWidgets.QVBoxLayout()
        layoutRight.addWidget(self.comboBox)
        layoutRight.addWidget(self.lcdNumber)

        layoutUp = QtWidgets.QHBoxLayout()
        layoutUp.addWidget(self.dial)
        layoutUp.addLayout(layoutRight)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(layoutUp)
        mainLayout.addWidget(self.slider)

        self.setLayout(mainLayout)
        self.setMinimumSize(400, 300)

    def initSignals(self) -> None:
        self.dial.valueChanged.connect(self.moveDial)
        self.slider.valueChanged.connect(self.moveSlider)
        self.comboBox.currentTextChanged.connect(self.comboBoxChanged)

    def comboBoxChanged(self) -> None:
        self.lcdNumber.display(self.transferVal(self.dial.value()))

    def moveDial(self) -> None:
        self.slider.setValue(self.dial.value())
        self.lcdNumber.display(self.transferVal(self.dial.value()))

    def moveSlider(self) -> None:
        self.dial.setValue(self.slider.value())
        self.lcdNumber.display(self.transferVal(self.slider.value()))

    def transferVal(self, num):
        if self.comboBox.currentText() == 'oct':
            return oct(num)
        if self.comboBox.currentText() == 'hex':
            return hex(num)
        if self.comboBox.currentText() == 'bin':
            return bin(num)
        else:
            return num

    def keyPressEvent(self, event: QtCore.QEvent) -> None:
        print(event.text(), QtCore.QEvent.Type.KeyPress, event.type())

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if watched == self.dial and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.text() == "+":
                self.dial.setValue(self.dial.value() + 1)
            if event.text() == "-":
                self.dial.setValue(self.dial.value() - 1)

        return super(Window, self).eventFilter(watched, event)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.settings.setValue("Number", self.dial.value())
        self.settings.setValue("CheckState", self.comboBox.currentText())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
