"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
from PySide6 import QtWidgets, QtCore, QtGui
from a_threads import SystemInfo


class SystemInfoWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initThreads()
        self.initUi()
        self.initSignals()

    def initThreads(self) -> None:
        self.threadSystemInfo = SystemInfo()
        self.threadSystemInfo.status = True
        self.threadSystemInfo.start()

    def initUi(self):
        font = self.font()
        font.setPointSize(12)

        # System info layout ------------------------------------------------------------------------------------------
        self.labelCPU = QtWidgets.QLabel("CPU:")

        self.lineEditCPU = QtWidgets.QLineEdit()
        self.lineEditCPU.setFont(font)
        self.lineEditCPU.setEnabled(False)

        self.labelRAM = QtWidgets.QLabel("RAM:")

        self.lineEditRAM = QtWidgets.QLineEdit()
        self.lineEditRAM.setFont(font)
        self.lineEditRAM.setEnabled(False)

        systemInfoLayout = QtWidgets.QHBoxLayout()
        systemInfoLayout.addWidget(self.labelCPU)
        systemInfoLayout.addWidget(self.lineEditCPU)
        systemInfoLayout.addWidget(self.labelRAM)
        systemInfoLayout.addWidget(self.lineEditRAM)

        # Set delay layout --------------------------------------------------------------------------------------------
        self.labelSetDelay = QtWidgets.QLabel("Set delay:")

        self.spinBoxSetDelay = QtWidgets.QSpinBox()

        setDelayLayout = QtWidgets.QHBoxLayout()
        setDelayLayout.addWidget(self.labelSetDelay)
        setDelayLayout.addWidget(self.spinBoxSetDelay)

        # Group box layout --------------------------------------------------------------------------------------------
        groupBoxLayout = QtWidgets.QVBoxLayout()
        groupBoxLayout.addLayout(systemInfoLayout)
        groupBoxLayout.addLayout(setDelayLayout)

        self.groupBoxSystemInfo = QtWidgets.QGroupBox("System Info")
        self.groupBoxSystemInfo.setLayout(groupBoxLayout)

        # Main layout -------------------------------------------------------------------------------------------------
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(self.groupBoxSystemInfo)

        self.setLayout(mainLayout)

    def initSignals(self) -> None:
        self.spinBoxSetDelay.valueChanged.connect(self.spinBoxChanged)
        self.threadSystemInfo.systemInfoReceived.connect(self.getSystemInfo)

    def spinBoxChanged(self) -> None:
        self.threadSystemInfo.delay = self.spinBoxSetDelay.value()

    def getSystemInfo(self, data: list) -> None:
        self.lineEditCPU.setText(f"{data[0]}%")
        self.lineEditRAM.setText(f"{data[1]}%")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.threadSystemInfo.status = False
        self.threadSystemInfo.wait(deadline=(self.threadSystemInfo.delay * 1000))
        self.threadSystemInfo.finished.connect(self.threadSystemInfo.deleteLater)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = SystemInfoWindow()
    window.show()

    app.exec()
