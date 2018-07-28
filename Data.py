# This class takes the input data and stores it

import numpy as np
from scipy.interpolate import UnivariateSpline as UVS
import time as time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading as pyth
from queue import Queue
from UniversalPiAPI import UZP
import ProjectConstants as c

# implement SPI interface with the Universal Pi Board and do I/O

sampleData = Queue(250500)
inittime = 0
LUTX = None
LUTY = None

uzp = UZP()

# This class will be controlling the continuous
# sine/sawtooth waves for the coil generators

class UZPOut:
    def __init__(self):
        # super().__init__(self)
        uzp.DACInit(c.XDAC)
        uzp.DACInit(c.YDAC)
        uzp.DACGenerate(c.XDAC, c.waveRes, self.mSine(c.waveRes, 4096), c.XHz)
        uzp.DACGenerate(c.YDAC, c.waveRes, self.mSawt(c.waveRes, 4096), c.YHz)

    # Returns a list of size numS that
    # traces a sine wave from 0 to amp
    def mSine(self, numS, amp):
        samples = []
        for i in range(numS):
            samples.append((amp / 2 * np.sin((i * 2 * c.pi) / numS) + amp / 2))
        return samples

    # Returns a list of size numS that
    # traces a sawtooth wave from 0 to amp
    def mSawt(self, numS, amp):
        samples = []
        for i in range(numS):
            samples.append(amp * i / numS)
        return samples

    def startGen(self):
        uzp.DACStart(c.XDAC)
        uzp.DACStart(c.YDAC)
        globals().inittime = time.perf_counter()

    def stopGen(self):
        uzp.DACStop(c.XDAC)
        uzp.DACStop(c.YDAC)


class UZPIn:
    # exitFlag = False
    sec = 0

    def __init__(self):
        # super().__init__()
        uzp.ADCInit(c.VADC)
        self.t = pyth.Timer(1.0, self.sample)

    def sample(self):
        databuff = uzp.ADCReadData([c.VADC], 1, c.SAMP_PER_CALL, c.bill / c.CALL_PERIOD)
        for i in range(c.SAMP_PER_CALL):
            # Stores time in nanoseconds
            sampleData.put((databuff[c.VADC][0][i], 39.1 + i * c.BETWEEN_TIME))
        self.sec = (self.sec + 1) % 10

    def start(self):
        self.t.start()

    def stop(self):
        self.t.cancel()


class TestData:
    # exitFlag = False
    sec = 0

    def __init__(self):
        self.stTime = 0

    def activate(self):
        self.sample()
        self.t = pyth.Timer(c.FREQ_OF_SAMPLE, self.activate)
        self.t.start()
        self.stTime = time.perf_counter()

    def sample(self):
        databuff = []
        for i in range(c.SAMP_PER_CALL):
            databuff.append(np.random.randint(255))

        for i in range(c.SAMP_PER_CALL):
            # Stores time in nanoseconds
            sampleData.put((databuff[i], 39.1 + i * c.BETWEEN_TIME))
        self.sec = (self.sec + 1) % 10

    def start(self):
        self.t = pyth.Timer(c.FREQ_OF_SAMPLE, self.activate)
        self.t.start()

    def stop(self):
        self.t.cancel()
