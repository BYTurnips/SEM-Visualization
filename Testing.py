import numpy as np
import scipy.interpolate as inter
import scipy.ndimage as ndi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import perf_counter
from collections import deque
from matplotlib import pyplot as plt


def fill(data, invalid=None):
    if invalid is None:
        invalid = np.isnan(data)

    ind = ndi.distance_transform_edt(invalid, return_distances=False, return_indices=True)
    print(ind)
    return data[tuple(ind)]


grid = np.asarray([[np.NaN, np.NaN, 1], [1, 2, 1], [np.NaN, np.NaN, np.NaN]])

print(grid)

print("What goes in: ")
print(np.isnan(grid))
print()
grid = fill(grid)

print(grid)
