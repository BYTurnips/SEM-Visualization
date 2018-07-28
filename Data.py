# This class takes the input data and stores it

import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading as pyth
from queue import Queue
from UniversalPiAPI import UZP
import ProjectConstants as c
# import RPi.GPIO as gpio

# implement SPI interface with the Universal Pi Board and do I/O

values = Queue(250500)
lock = QMutex()
scanData = np.zeros((c.defw, c.defh, c.SAMP_PER_PIX))
displayData = np.zeros((c.defw, c.defh))

# uzp = UZP()

# This class will be controlling the continuous
# sine/sawtooth waves for the coil generators

# class UZPOut:
#     def __init__(self):
#         # super().__init__(self)
#         uzp.DACInit(c.XDAC)
#         uzp.DACInit(c.YDAC)
#         uzp.DACGenerate(c.XDAC, c.waveRes, self.mSine(c.waveRes, 4096), c.XHz)
#         uzp.DACGenerate(c.YDAC, c.waveRes, self.mSawt(c.waveRes, 4096), c.YHz)
#
#     # Returns a list of size numS that
#     # traces a sine wave from 0 to amp
#     def mSine(self, numS, amp):
#         samples = []
#         for i in range(numS):
#             samples.append((amp/2 * np.sin((i * 2 * c.pi)/numS) + amp/2))
#         return samples
#
#     # Returns a list of size numS that
#     # traces a sawtooth wave from 0 to amp
#     def mSawt(self, numS, amp):
#         samples = []
#         for i in range(numS):
#             samples.append(amp * i/numS)
#         return samples
#
#     def startGen(self):
#         uzp.DACStart(c.XDAC)
#         uzp.DACStart(c.YDAC)
#
#     def stopGen(self):
#         uzp.DACStop(c.XDAC)
#         uzp.DACStop(c.YDAC)

# class UZPIn:
#     # exitFlag = False
#     sec = 0
#
#     def __init__(self):
#         # super().__init__()
#         uzp.ADCInit(c.VADC)
#         self.t = pyth.Timer(1.0, self.sample)
#
#     def sample(self):
#         databuff = uzp.ADCReadData([c.VADC], 1, c.SAMP_PER_CALL, 100)
#         for i in range(c.SAMP_PER_CALL):
#             # Stores time in nanoseconds
#             values.put((databuff[c.VADC][0][i], 39.1+i*c.CALL_PERIOD/c.SAMP_PER_CALL))
#         self.sec = (self.sec + 1) % 10
#
#     def start(self):
#         self.t.start()
#
#     def stop(self):
#         self.t.cancel()




class TestData(QThread):
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

        # self.round += 1
        # if self.round == 25:
        #     for i in range(2500 * 25):
        #         p = QPainter()
        #         p.begin(self.scanA)
        #         t = displayData[self.sx][self.sy]
        #         p.setPen(QColor(t, t, t, 255))
        #         p.drawPoint(self.sx, self.sy)
        #         p.end()
        #         self.sx += 1
        #         if self.sx == c.defw:
        #             self.sx = 0
        #             self.sy += 1
        #         if self.sy == c.defh:
        #             self.sy = 0
        #     print("Finished Image...")
        #     self.loadedImage.emit(self.scanA)
        #     self.round = 0
        return
