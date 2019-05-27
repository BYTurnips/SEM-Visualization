# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will locate every line, then "straighten" the lines using the average function
# Afterwards, it will take the new lines and arrange them so they closely match a square grid
# with the same rough orientation and size (via average area, average slope of lines)
# this whole transform changes an LUT of each region's upper right corner, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
import scipy as sp
import skimage as ski
import skimage.morphology as morph
import skimage.util as util
import matplotlib.pyplot as plt
from skimage.feature import canny
from PyQt5.QtGui import *

class GridFinder:
    def __init__(self):
        fig, self.axes = plt.subplots(1, 3)
        self.initImage = ski.io.imread('Init_250.bmp', as_gray=True)
        inv = util.invert(self.initImage)
        self.axes[0].imshow(inv, cmap=plt.cm.gray, interpolation='nearest')
        inv = morph.erosion(inv, selem=np.ones((3, 3)))
        self.axes[1].imshow(inv, cmap=plt.cm.gray, interpolation='nearest')
        self.diagnoseLine(self.initImage)
        plt.show()

    def diagnoseLine(self, img):
        self.out, self.angles, self.dists = ski.transform.hough_line(img)


if __name__ == "__main__":
    g = GridFinder()
