import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from scanArea import *
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
        quitb = QPushButton('Quit', self)
        quitb.clicked.connect(QApplication.instance().quit)
        quitb.resize(quitb.sizeHint())
        quitb.move(defw-150, 60)
        scanb = QPushButton('Start Scan', self)
        scanb.clicked.connect(Application.paintit)
        # scanb.clicked.connect(Application.saystuff)
        scanb.resize(scanb.sizeHint())
        scanb.move(defw - 150, 120)
        self.paintit()
        print("Ready to go!")

        self.setFixedWidth(defw)
        self.setFixedHeight(defh)
        self.setWindowTitle('SEM Visualization Demo')
        self.show()

    def paintit(self):
        print("Hi!")
        self.update()
    def paintEvent(self, event):
        scanarea = QStylePainter()
        scanarea.begin(self)
        scanarea.drawPoint(50, 50)

        for i in range(50, 550):
            for j in range(50, 550):
                scanarea.drawPoint(i, j)
        scanarea.setPen(QColor(self.r, self.g, self.b, 255))
        self.r += 10
        self.g += 10
        self.b += 10
        scanarea.end()

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