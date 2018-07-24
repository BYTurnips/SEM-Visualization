# This class starts the application and handles everything

import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from QTD_Window import Ui_MainWindow
import Data as data
import Display as display
import Gui as gui


class master(QObject):
    startScanning = pyqtSignal()
    endScanning = pyqtSignal()
    sendImage = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = gui.GUI()
        self.displayTh = display.display()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTh.start)

        self.window.startScanning.connect(self.timer.start)
        self.window.endScanning.connect(self.timer.stop)
        self.displayTh.loadedImage.connect(self.relayImage)
        self.sendImage.connect(self.window.showGivenImage)
        self.dataTh = data.AnalogData()
        self.window.show()
        sys.exit(self.app.exec_())

    def relayImage(self, image):
        print("Relaying Image")
        self.sendImage.emit(image)
        return

    def saystuff(self):
        print("HI")


if __name__ == "__main__":
    c = master()
