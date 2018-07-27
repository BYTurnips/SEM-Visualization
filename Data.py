# This class takes the input data and stores it

import numpy as np
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# import RPi.GPIO as gpio

#implement SPI interface with the ADC and set up the call function

SAMP_PER_PIX = 1
lock = QMutex()
scanData = np.zeros((500, 500, SAMP_PER_PIX))
displayData = np.zeros((500, 500))


class UZPData(QThread):
    def __init__(self):
        super().__init__()
        self.scanA = QImage('Static_BG.JPG')



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
        self.scanA = QImage('Static_BG.JPG')

    def increment(self):
        self.x += 1
        if self.x == 500:
            self.x = 0
            self.y += 1
        if self.y == 500:
            self.y = 0
            self.z += 1
        if self.z == SAMP_PER_PIX:
            self.z = 0

    def run(self):
        # Incomplete; breaks when scanning multiple times between displays
        q = QMutexLocker(lock)
        if self.round == 1:
            self.sx = self.x
            self.sy = self.y

        for i in range(2500):
            scanData[self.x][self.y][self.z] = np.random.randint(0, 256)
            displayData[self.x][self.y] = np.sum(scanData[self.x][self.y]) / SAMP_PER_PIX
            self.increment()

        if self.round == 10:
            for i in range(2500 * 10):
                p = QPainter()
                p.begin(self.scanA)
                t = displayData[self.sx][self.sy]
                p.setPen(QColor(t, t, t, 255))
                p.drawPoint(self.sx, self.sy)
                p.end()
                self.sx += 1
                if self.sx == 500:
                    self.sx = 0
                    self.sy += 1
                if self.sy == 500:
                    self.sy = 0
            print("Finished Image...")
            self.loadedImage.emit(self.scanA)
            self.round = 0
        self.round += 1
        return
