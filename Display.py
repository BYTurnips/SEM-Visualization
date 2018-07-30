# This class processes the data present in the data storage
# and displays the result in the scanArea

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ProjectConstants as c
import Data as data
import numpy as np
import timeit
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
    def __init__(self):
        super().__init__()
        self.scanA = c.IMG.copy(0, 0, c.defw, c.defh)


    def run(self):
        p = QPainter()
        p.begin(self.scanA)
        print("Displaying")
        # print(data.sampleData.__sizeof__())
        # a = timeit.timeit()
        for i in range(c.PIX_PER_UPDATE):
            # tsvalue = data.sampleData.get()
            tsvalue = data.sampleData.popleft()
            t = 100
            t = tsvalue[1]
            v = 0
            v = tsvalue[0]
            p.setPen(QColor(v, v, v, 255))
            # p.drawPoint(np.rint(data.LUTX(t % (c.bill / c.XHz))), (np.rint(data.LUTY(t) * 4)))
            plotx = gen.TriaLUT(t % (c.bill / c.XHz), c.defw, c.bill / c.XHz)
            ploty = gen.SawtLUT(t, c.defh, c.bill / c.YHz) * 4
            # print(plotx, ploty, t)
            p.drawPoint(np.rint(plotx), np.rint(ploty))
        p.end()
        # print(timeit.timeit()-a)
        print("Finished Image...")
        self.loadedImage.emit(self.scanA)

    def saystuff(self):
        print("HI")
