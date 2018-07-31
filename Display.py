# This class processes the data present in the data storage
# and displays the result in the scanArea

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ProjectConstants as c
import Data as data
import numpy as np
from time import perf_counter
from math import floor
from WaveGen import UZPOut as gen


class UZPdisplay(QThread):
    notCancelling = True
    loadedImage = pyqtSignal(QImage)

    x = 0
    y = 0

    def __init__(self):
        super().__init__()
        self.scanA = c.IMG.copy(0, 0, c.defw, c.defh)

    def run(self):
        p = QPainter()
        p.begin(self.scanA)
        print("Displaying")
        print(data.sampleData.qsize())
        for i in range(c.PIX_PER_UPDATE):
            # t = data.displayData[i][j]
            tsvalue = data.sampleData.get()
            t = 100
            t = tsvalue[1]
            v = 200
            v = tsvalue[0]  # * 255 / c.SAMP_PER_CALL
            # print(v)
            p.setPen(QColor(v, v, v, 255))
            p.drawPoint(self.x, self.y)
            self.x += 1
            if (self.x == 500):
                self.x = 0
                self.y += 1
            if (self.y == 500):
                self.y = 0
        p.end()
        print("Finished Image...")
        self.loadedImage.emit(self.scanA)

    def saystuff(self):
        print("HI")


class display(QThread):
    notCancelling = True
    loadedImage = pyqtSignal(QImage)
    cur = 0
    def __init__(self):
        super().__init__()
        self.scanA = c.IMG.copy(0, 0, c.defw, c.defh)
        self.ColorsLUT = []
        for i in range(256):
            self.ColorsLUT.append(QColor(i, i, i, 255))


    def run(self):
        # p = QPainter()
        # p.begin(self.scanA)
        print("Displaying")
        print(len(data.sampleData))
        testing = perf_counter()
        for i in range(c.PIX_PER_UPDATE):
            # tsvalue = data.sampleData.get()
            try:
                tsvalue = data.sampleData.popleft()
            except:
                break
            t = tsvalue[1]
            v = tsvalue[0]
            # v = self.cur
            # p.setPen(QColor(v, v, v, 255))
            # p.setPen(self.ColorsLUT[v])
            plotx = gen.TriaLUT(t % (c.bill / c.XHz), c.defw, c.bill / c.XHz)
            ploty = gen.SawtLUT(t, c.defh, c.bill / c.YHz)
            # print(plotx, ploty, t)
            # p.drawPoint(np.rint(plotx), np.rint(ploty))
            self.scanA.setPixelColor(np.rint(plotx), np.rint(ploty), self.ColorsLUT[v])
        # p.end()
        print("Generating Image:", perf_counter() - testing)
        print("Finished Image...")
        self.loadedImage.emit(self.scanA)
        self.cur = (self.cur + 40) % 255

    def saystuff(self):
        print("HI")
