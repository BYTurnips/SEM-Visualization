import numpy as np
from PyQt5.QtGui import *
from WaveGen import UZPOut as gen
from scipy.interpolate import InterpolatedUnivariateSpline as uvs
import ProjectConstants as c
from time import perf_counter


if __name__ == "__main__":
    ColorsLUT = []
    for i in range(256):
        ColorsLUT.append(QColor(i, i, i, 255))
    print("BEGIN")
    gen.generateLUT()
    scanA = QImage()
    p = QPainter()
    p.begin(scanA)
    cl = Data.TestData()
    time = perf_counter()
    for i in range(100):
        cl.sample()
    print("Sampling:", perf_counter() - time)
    time = perf_counter()
    print("Displaying")
    for i in range(c.PIX_PER_UPDATE):
        tsvalue = Data.sampleData.popleft()
        t = tsvalue[1]
        v = tsvalue[0]
        p.setPen(QColor(v, v, v, 255))
        # print(data.LUTX(t % (c.bill / c.XHz)), " ", data.LUTY(t) * 4, t)
        plotx = gen.TriaLUT(t % (c.bill / c.XHz), c.defw, c.bill / c.XHz)
        ploty = gen.SawtLUT(t, c.defh, c.bill / c.YHz) * 4
        # print(plotx, ploty, t)
        p.drawPoint(np.rint(plotx), np.rint(ploty))

    print("Full:", perf_counter() - time)
    time = perf_counter()

    for i in range(c.PIX_PER_UPDATE):
        tsvalue = Data.sampleData.popleft()
        t = tsvalue[1]
        v = tsvalue[0]

    print("Pop from buffer:", perf_counter() - time)
    time = perf_counter()

    for i in range(c.PIX_PER_UPDATE):
##        p.setPen(QColor(0, 0, 0, 255)
        color = ColorsLUT[8]
        p.setPen(color)

    print("Set Pen:", perf_counter() - time)
    time = perf_counter()

    fakelutx = uvs([0, 1],[0, 1], k=1)
    fakeluty = uvs([0, 1],[0, 1], k=1)

    for i in range(c.PIX_PER_UPDATE):
##        a = data.LUTX(0 % (c.bill / c.XHz))
##        b = data.LUTY(0) * 4
        a = fakelutx(0)
        b = fakeluty(0)
##        plotx = gen.TriaLUT(t % (c.bill / c.XHz), c.defw, c.bill / c.XHz)
##        ploty = gen.SawtLUT(t, c.defh, c.bill / c.YHz) * 4


    print("Use LUT or conversion:", perf_counter() - time)
    time = perf_counter()

##    for i in range(c.PIX_PER_UPDATE):
##        a = np.sin(78)
##        b = np.sin(24.9)
##
##    print("Use sine:", perf_counter() - time)
##    time = perf_counter()

    for i in range(c.PIX_PER_UPDATE):
        a = int(0.2780)
        b = int(0.5798)

    print("Floor Coordinate:", perf_counter() - time)
    time = perf_counter()

    for i in range(c.PIX_PER_UPDATE):
        p.drawPoint(0, 0)
    print("Draw Point:", perf_counter() - time)

    p.end()
    # print(timeit.timeit()-a)
    print("Finished Image...")
