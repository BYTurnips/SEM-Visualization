# This class takes the input data and stores it

import numpy as np
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ProjectConstants as c
# import RPi.GPIO as gpio

#implement SPI interface with the ADC and set up the call function

lock = QMutex()
scanData = np.zeros((c.defw, c.defh, c.SAMP_PER_PIX))
displayData = np.zeros((c.defw, c.defh))


class UZPData(QThread):
    def __init__(self):
        super().__init__()
        self.scanA = c.IMG.copy(0, 0, c.defw, c.defh)



class AnalogData(QThread):
    loadedImage = pyqtSignal(QImage)
    x = 0
    y = 0
    z = 0

    sx = 0
    sy = 0

    round = 0

    def __init__(self):
        super().__init__()
        self.scanA = c.IMG.copy(0, 0, c.defw, c.defh)

    def increment(self):
        self.x += 1
        if self.x == c.defw:
            self.x = 0
            self.y += 1
        if self.y == c.defh:
            self.y = 0
            self.z += 1
        if self.z == c.SAMP_PER_PIX:
            self.z = 0

    def run(self):
        # Incomplete; breaks when scanning multiple times between displays
        q = QMutexLocker(lock)
        if self.round == 0:
            self.sx = self.x
            self.sy = self.y

        for i in range(2500):
            scanData[self.x][self.y][self.z] = np.random.randint(0, 256)
            displayData[self.x][self.y] = np.sum(scanData[self.x][self.y]) / c.SAMP_PER_PIX
            self.increment()

        self.round += 1
        if self.round == 20:
            for i in range(2500 * 20):
                p = QPainter()
                p.begin(self.scanA)
                t = displayData[self.sx][self.sy]
                p.setPen(QColor(t, t, t, 255))
                p.drawPoint(self.sx, self.sy)
                p.end()
                self.sx += 1
                if self.sx == c.defw:
                    self.sx = 0
                    self.sy += 1
                if self.sy == c.defh:
                    self.sy = 0
            print("Finished Image...")
            self.loadedImage.emit(self.scanA)
            self.round = 0
        return
