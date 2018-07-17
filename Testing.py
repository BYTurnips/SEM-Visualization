# This class generates the responsive UI capabilities of the application
# and acts as the main starter for all other threads

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

defw = 1000
defh = 600


class compute(QThread):

    def __init__(self, scanA):
        QThread.__init__(self)
        self.r = 0
        self.g = 0
        self.b = 0
        self.scanA = scanA

    def run(self):
        p = QPainter()
        p.begin(self.scanA)
        # p.fillRect(0, 0, 500, 500, QColor(self.r, self.g, self.b, 250))
        p.setPen(QColor(self.r, self.g, self.b, 250))
        for i in range(500):
            for j in range(500):
                p.drawPoint(i, j)
        self.r = (self.r + 40) % 255
        self.g = (self.g + 40) % 255
        self.b = (self.b + 40) % 255
        p.end()
        self.emit(SIGNAL('LoadedImage()'), )
        return


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scanA = QImage('Yellow_BG.JPG')
        self.scanPixmap = QPixmap()
        self.scanLabel = QLabel('Scan Area', self)

        self.computer = compute()
        self.computer.start()

        self.initUI()
        self.initFuncs()

    def showImage(self):
        self.scanPixmap.convertFromImage(self.scanA)
        self.scanLabel.setPixmap(self.scanPixmap)
        return

    def drawImage(self):
        p = QPainter()
        p.begin(self.scanA)
        # p.fillRect(0, 0, 500, 500, QColor(self.r, self.g, self.b, 250))
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

            self.showImage()

    def initFuncs(self):
        self.drawImage()
        self.showImage()
        self.scanLabel.move(50, 50)
        self.scanLabel.show()

        self.connect(self.computer, SIGNAL(""))

    def initUI(self):
        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(defw - 150, 60)

        scanb = QPushButton('Start Scan', self)
        scanb.clicked.connect(self.updateImage)

        scanb.resize(scanb.sizeHint())
        scanb.move(defw - 150, 120)

        self.setFixedWidth(defw)
        self.setFixedHeight(defh)
        self.setWindowTitle('SEM Visualization Demo')
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
