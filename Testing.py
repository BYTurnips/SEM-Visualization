import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import perf_counter
from collections import deque


if __name__ == '__main__':
    scanA = QImage("grid.png")
    p = QPainter(scanA)
    ColorsLUT = []
    #     for i in range(256):
    #         ColorsLUT.append(QColor(i, i, i, 255))
    #     time = perf_counter()
    #     for i in range(500):
    #         for j in range(500):
    #             color = QColor(0, 10, 20, 255)
    # ##            color = ColorsLUT[8]
    #     print("Make Color:", perf_counter() - time)
    #     time = perf_counter()
    #     fix = QColor(0, 0, 0)
    #     for i in range(500):
    #         for j in range(500):
    #             p.setPen(fix)
    #     print("Change Pen:", perf_counter() - time)
    #     time = perf_counter()
    #     for i in range(500):
    #         for j in range(500):
    #             p.drawPoint(i, j)
    #     print("Draw Pixel:", perf_counter() - time)
    #     time = perf_counter()
    #     for i in range(500):
    #         for j in range(500):
    #             scanA.setPixelColor(i, j, color)
    #     print("Set Pixel:", perf_counter() - time)
    h = deque(maxlen=250500)
    for i in range(250500):
        h.append(0)
    time = perf_counter()
    h.clear()
    print(perf_counter() - time)
