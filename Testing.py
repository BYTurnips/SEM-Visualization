# This class generates the responsive UI capabilities of the application
# and acts as the main starter for all other threads

import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# I might be misunderstanding how mutex works...do the mutex objects have to be the same
# each time they're called?
# Can change image to grayscale
scanData = np.zeros((500, 500, 5))
displayData = np.zeros((500, 500))

class data(QThread):
    x = 0
    y = 0
    z = 0

    def __init__(self):
        super().__init__()
        self.lock = QMutex()

    def run(self):
        q = QMutexLocker(self.lock)
        for i in range(2500):
            scanData[self.x][self.y][self.z] = np.randint(0, 256)
            displayData[self.x][self.y] = np.sum(scanData[self.x][self.y]) / 5
            self.x += 1
            if self.x == 500:
                self.x = 0
                self.y += 1
            if self.y == 500:
                self.y = 0
                self.z += 1
            if self.z == 5:
                self.z = 0
        return


class display(QThread):
    loadedImage = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.lock = QMutex()

    def run(self):
        # q = QMutexLocker(self.lock)
        scanA = QImage('Yellow_BG.JPG')
        p = QPainter()
        p.begin(scanA)
        for i in range(500):
            for j in range(500):
                t = displayData[i][j]
                p.setPen(QColor(t, t, t, 255))
                p.drawPoint(i, j)
        p.end()
        for i in range(500):
            print("HIIII")
        self.loadedImage.emit(scanA)
        return


class setUI(object):
    def setupUI(self, MainWindow):
        MainWindow.setObjectName("Testing Window")
        MainWindow.resize(1000, 650)
        MainWindow.setMinimumSize(QSize(1000, 600))
        MainWindow.setMaximumSize(QSize(1000, 600))
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.ScanB = QPushButton(self.centralWidget)
        self.ScanB.setGeometry(QRect(630, 50, 131, 31))
        self.ScanB.setCheckable(True)
        self.ScanB.setObjectName("ScanB")


class GUI(QMainWindow):
    startScanning = pyqtSignal()
    defw = 1000
    defh = 600
    r = 0
    g = 0
    b = 0

    def __init__(self):
        super().__init__()
        self.scanA = QImage('Yellow_BG.JPG')
        self.scanPixmap = QPixmap()
        self.scanLabel = QLabel('Scan Area', self)
        self.scanLabel.setFixedSize(500, 500)
        self.initUI()

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
        p.setPen(QColor(self.r, self.g, self.b, 250))
        for i in range(500):
            for j in range(500):
                p.drawPoint(i, j)
        self.r = (self.r + 40) % 255
        self.g = (self.g + 40) % 255
        self.b = (self.b + 40) % 255
        p.end()
        return

    def updateImage(self):
        for i in range(10):
            self.drawImage()
            self.showImage()

    def initUI(self):
        self.drawImage()
        self.showImage()
        self.scanLabel.move(50, 50)
        self.scanLabel.show()

        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(self.defw - 150, 60)

        scanb = QPushButton('Start Scan', self)
        scanb.clicked.connect(self.startScanning.emit)

        scanb.resize(scanb.sizeHint())
        scanb.move(self.defw - 150, 120)

        self.setFixedWidth(self.defw)
        self.setFixedHeight(self.defh)
        self.setWindowTitle('SEM Visualization Demo')
        self.show()


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
        self.setu = setUI()
        self.setu.setupUI(self.window)
        self.displayTh = display()

        self.window.startScanning.connect(self.displayTh.start)
        self.displayTh.loadedImage.connect(self.relayImage)
        self.sendImage.connect(self.window.showGivenImage)
        self.dataTh = data()

        self.window.show()
        sys.exit(self.app.exec_())

    def relayImage(self, image):
        print("Relaying Image")
        self.sendImage.emit(image)
        return



if __name__ == "__main__":
    c = master()
