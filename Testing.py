import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import perf_counter


if __name__ == '__main__':
    scanA = QImage("grid.png")
    p = QPainter(scanA)
    time = perf_counter()
    for i in range(500):
        for j in range(500):
            p.drawPoint(i, j)
    print(perf_counter() - time)
    time = perf_counter()
    for i in range(500):
        for j in range(500):
            color = QColor(0, 10, 20, 255)
            # p.setPen(QColor(0, 10, 20, 255))
            # p.drawPoint(i, j)
    print(perf_counter() - time)
    time = perf_counter()
    fix = QColor(0, 0, 0)
    for i in range(500):
        for j in range(500):
            p.setPen(fix)
    print(perf_counter() - time)
    time = perf_counter()
