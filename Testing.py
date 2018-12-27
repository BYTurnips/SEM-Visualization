import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from time import perf_counter
from collections import deque
from matplotlib import pyplot as plt

if __name__ == '__main__':
    _, axes = plt.subplots(1, 4, figsize=(8, 3), sharey=True)
    xs = [30]
    ys = [100]
    x = 30
    y = 30

    axes[0].scatter(x, y)
    plt.show()
