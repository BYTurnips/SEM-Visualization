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
    def initUI(self):
        scanA = QImage(500, 500, 24)
        scanPaint = QPainter(scanA)
        scanPixmap = QGraphicsPixmapItem()
        scanPixmap.setPixmap()
        scanScene = QGraphicsScene()
        scanScene.addPixmap(scanPixmap)
        scanView = QGraphicsView(scanScene)
        scanView.show()

        scanPaint.drawRect(50, 50, 50, 50)

        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(defw-150, 60)

        scanb = QPushButton('Start Scan', self)
        scanb.clicked.connect(scanArea.paintit)

        scanb.resize(scanb.sizeHint())
        scanb.move(defw - 150, 120)
        self.paintit()
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