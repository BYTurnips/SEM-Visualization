import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

defw = 1000
defh = 600

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(defw-150, 60)
        scanb = QPushButton('Start Scan', self)
        scanb.clicked.connect(QApplication.instance().quit)
        scanb.resize(scanb.sizeHint())
        scanb.move(defw - 150, 120)

        inArea = QPainter()
        inArea.drawPoint(50, 50)
        self.setFixedWidth(defw)
        self.setFixedHeight(defh)
        self.setWindowTitle('SEM Visualization Demo')
        self.show()

    def initScan(self):
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())