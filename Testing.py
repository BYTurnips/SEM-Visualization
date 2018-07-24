# This class generates the responsive UI capabilities of the application
# and acts as the main starter for all other threads

import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from QTD_Window import Ui_MainWindow
import Data as data

# I might be misunderstanding how mutex works...do the mutex objects have to be the same
# each time they're called?
# Can change image to grayscale

class display(QThread):
    notCancelling = True
    loadedImage = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

    def run(self):
        q = QMutexLocker(data.lock)
        t = random.randint(0, 256)
        scanA = QImage('Yellow_BG.JPG')
        p = QPainter()
        p.begin(scanA)
        for i in range(500):
            for j in range(500):
                # t = displayData[i][j]
                p.setPen(QColor(t, t, t, 255))
                p.drawPoint(i, j)
        p.end()
        print("Finished Image...")
        self.loadedImage.emit(scanA)

    def saystuff(self):
        print("HI")

class GUI(QMainWindow):
    startScanning = pyqtSignal()
    endScanning = pyqtSignal()
    defw = 1000
    defh = 600

    def __init__(self):
        super().__init__()
        self.scanA = QImage('Yellow_BG.JPG')
        self.scanPixmap = QPixmap()
        self.scanLabel = QLabel('Scan Area', self)
        self.scanLabel.setFixedSize(500, 500)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.drawImage()
        self.showImage()
        self.scanLabel.move(50, 90)
        self.scanLabel.show()
        self.connectUI()


    def showImage(self):
        self.scanPixmap.convertFromImage(self.scanA)
        self.scanLabel.setPixmap(self.scanPixmap)
        return

    def showGivenImage(self, image):
        self.scanPixmap.convertFromImage(image)
        self.scanLabel.setPixmap(self.scanPixmap)
        return

    def drawImage(self):
        p = QPainter()
        p.begin(self.scanA)
        p.setPen(QColor(0, 0, 0, 250))
        for i in range(500):
            for j in range(500):
                p.drawPoint(i, j)
        p.end()
        return

    def updateImage(self):
        for i in range(10):
            self.drawImage()
            self.showImage()

    def connectUI(self):
        self.ui.ScanB.clicked.connect(self.toggleScanning)

    def toggleScanning(self, active):
        if active:
            self.startScanning.emit()
        else:
            self.endScanning.emit()

    def saystuff(self, val):
        print("HI")

# all you have to do now is connect the mainwindow "start work" sig to the master slot
# which then starts a display thread. the display thread will periodically emit
# a signal connected to another master slot that emits a signal to the window slot
# that displays the image........hope this works
class master(QObject):
    startScanning = pyqtSignal()
    endScanning = pyqtSignal()
    sendImage = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = GUI()
        self.displayTh = display()

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
