import numpy as np
from PyQt5.QtCore import *

ndarray = np.zeros((500, 500, 5))
lock = QMutex()
if __name__ == "__main__":
    locker = QMutexLocker(lock)
    for i in range(500):
        for j in range(500):
            for k in range(5):
                ndarray[i][j][k] = np.random.randint(0, 256)
    print(ndarray[0][0][0])
