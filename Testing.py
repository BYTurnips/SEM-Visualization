import numpy as np
import scipy.interpolate as inter
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import perf_counter
from collections import deque
from matplotlib import pyplot as plt


# # x = np.arange(0, 5, 1)
# # y = np.arange(0, 5, 1)
# x = np.asarray([0, 1, 2, 3, 4])
# y = np.asarray([0, 1, 2, 3, 4])
# xx, yy = np.meshgrid(x, y)
# # z = np.sin(xx*2+yy*2)
# z = np.asarray([[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]])
# f = inter.interp2d(x, y, z)

def func(x, y):
    return x + y


grid_x, grid_y = np.mgrid[0:25:6j, 0:25:6j]
points = np.random.rand(10, 2) * 25
points = points.astype(int)
values = func(points[:, 0], points[:, 1])

# print(points)
# print(values)

grid = inter.griddata(points, values, (grid_x, grid_y))

row = np.mgrid[0:25:6j]
col = np.mgrid[0:25:6j]

print(row)
print(col)
print(grid)
lut = inter.interp2d(row, col, grid)
