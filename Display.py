# This class processes the data present in the data storage
# and displays the result in the scanArea

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Data as data


class display(QThread):
    notCancelling = True
    loadedImage = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.lock = QMutex()

    def run(self):
        self.notCancelling = True
        q = QMutexLocker(self.lock)
        t = 0
        while self.notCancelling:
            scanA = QImage('Yellow_BG.JPG')
            p = QPainter()
            p.begin(scanA)
            t = (t + 40) % 255
            for i in range(500):
                for j in range(500):
                    # t = displayData[i][j]
                    p.setPen(QColor(t, t, t, 255))
                    p.drawPoint(i, j)
            p.end()
            print("Finished Image...")
            self.loadedImage.emit(scanA)
