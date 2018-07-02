import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

defw = 1000
defh = 600


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    r = 50
    g = 50
    b = 50

    def initUI(self):
        quitb = QPushButton('Redraw', self)
        quitb.clicked.connect(Application.paintit)
        quitb.resize(quitb.sizeHint())
        quitb.move(defw - 150, 60)

        self.setFixedWidth(defw)
        self.setFixedHeight(defh)
        self.setWindowTitle('Refresh Problem')
        self.show()

    def paintit(self):
        self.update()

    def paintEvent(self, event):
        scanarea = QStylePainter()
        scanarea.begin(self)
        print("yo I'm painting")
        print(self.r)
        print(self.g)
        print(self.b)
        scanarea.drawPoint(self.r + 50, self.g + 50)

        # for i in range(50, 550):
        #     for j in range(50, 550):
        #         scanarea.drawPoint(i, j)
        # scanarea.setPen(QColor(self.r, self.g, self.b, 0))
        self.r += 1
        if self.r > 250: self.r = 0
        self.g += 1
        if self.g > 250: self.g = 0
        self.b += 1
        if self.b > 250: self.b = 0
        scanarea.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
