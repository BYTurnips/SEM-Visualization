# This class processes the data present in the data storage
# and displays the result in the scanArea

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ProjectConstants as c
import Data as data


class display(QThread):
    notCancelling = True
    loadedImage = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.scanA = c.IMG.copy(0, 0, c.defw, c.defh)


    def run(self):
        q = QMutexLocker(data.lock)
        p = QPainter()
        p.begin(self.scanA)
        for i in range(c.defw):
            for j in range(c.defh):
                t = data.displayData[i][j]
                p.setPen(QColor(t, t, t, 255))
                p.drawPoint(i, j)
        p.end()
        print("Finished Image...")
        self.loadedImage.emit(self.scanA)

    def saystuff(self):
        print("HI")
