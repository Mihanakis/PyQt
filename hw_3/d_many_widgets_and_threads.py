"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets, QtGui
from b_systeminfo_widget import SystemInfoWindow
from c_weatherapi_widget import GetWeatherWindow


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle("Many Widgets")

        self.systemInfoWidget = SystemInfoWindow()
        self.weatherInfoWidget = GetWeatherWindow()

        # layout -------------------------------------------------------------
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.systemInfoWidget)
        layout.addWidget(self.weatherInfoWidget)

        self.setLayout(layout)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.systemInfoWidget.close()
        self.weatherInfoWidget.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
