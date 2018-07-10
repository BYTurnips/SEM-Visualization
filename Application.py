import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from scanArea import scanArea
from Data import AnalogData as input

defw = 1000
defh = 600


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    r = 0
    g = 0
    b = 0
    scanA = QImage('Yellow_BG.JPG')

    def showImage(self):
        return

    def drawImage(self):
        p = QPainter(self.scanA)
        for i in range(500):
            p.setPen(QColor(i / 2, i / 2, i / 2, 255))
            p.drawLine(i, 0, i, 500)
        p.drawRect(0, 0, 500, 500)
        return
    def initUI(self):
        self.drawImage()
        scanPixmap = QPixmap()
        scanPixmap.convertFromImage(self.scanA)
        scanLabel = QLabel('Scan Area', self)
        scanLabel.setPixmap(scanPixmap)
        scanLabel.resize(scanLabel.sizeHint())
        scanLabel.move(50, 50)
        scanLabel.show()
        # scanLabel.deleteLater()
        # self.scanPaint.setPen(QColor(50, 50, 50, 50))
        # self.scanPaint.drawRect(50, 50, 50, 50)
        # scanPixmap.convertFromImage(self.scanA)
        # scanLabel2 = QLabel('Scan Area', self)
        # scanLabel2.setPixmap(scanPixmap)
        # scanLabel2.move(100, 100)
        # scanLabel2.show()

        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(defw-150, 60)

        scanb = QPushButton('Start Scan', self)
        # scanb.clicked.connect(self.drawImage())

        scanb.resize(scanb.sizeHint())
        scanb.move(defw - 150, 120)
        print("Ready to go!")

        self.setFixedWidth(defw)
        self.setFixedHeight(defh)
        self.setWindowTitle('SEM Visualization Demo')
        self.show()

    def startScan(self):
        return
    def stopScan(self):
        return
    def saystuff(self):
        print("Button was clicked")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())