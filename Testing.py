# This class generates the responsive UI capabilities of the application
# and acts as the main starter for all other threads

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class data(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        print("hIihihi")
        return

class compute(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(1000000):
            print("HIHIHIHIHI\n")
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
    defw = 1000
    defh = 600

    def __init__(self):
        super().__init__()
        self.scanA = QImage('Yellow_BG.JPG')
        self.scanPixmap = QPixmap()
        self.scanLabel = QLabel('Scan Area', self)
        self.scanLabel.setFixedSize(500, 500)
        self.initUI()

    r = 0
    g = 0
    b = 0

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

        self.drawImage()
        self.showImage()

        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(self.defw - 150, 60)

        scanb = QPushButton('Start Scan', self)
        scanb.clicked.connect(self.updateImage)

        # all you have to do now is connect the mainwindow "start work" sig to the master slot
        # which then starts a compute thread. the compute thread will periodically emit
        # a signal connected to another master slot that emits a signal to the window slot
        # that displays the image........hope this works

        scanb.resize(scanb.sizeHint())
        scanb.move(self.defw - 150, 120)

        self.setFixedWidth(self.defw)
        self.setFixedHeight(self.defh)
        self.setWindowTitle('SEM Visualization Demo')
        self.show()


class master():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = GUI()
        self.setu = setUI()
        self.setu.setupUI(self.window)
        self.displayTh = compute()
        self.displayTh.start()
        self.dataTh = data()

        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    c = master()
