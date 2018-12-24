# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will locate every white region and grab the upper-right most point of that region.
# This yields a "grid" of points that is slightly warped. Using [SOME ALGORITHM], a grid of
# the correct orientation is matched to this point grid.
# this whole transform changes an LUT of each region's upper right corner, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
import scipy as sp
import skimage as ski
from PyQt5.QtGui import *

LUT = []


class RegionFinder:
    def __init__(self):
        self.initImage = ski.io.imread('Init_250.bmp', as_gray=True)
        # self.diagnoseLine(self.initImage)
        self.out, self.angles, self.dists = ski.transform.hough_line(self.initImage)
        print(self.angles)
        print(self.dists)

    def diagnoseLine(self, img):
        self.out, self.angles, self.dists = ski.transform.hough_line(img)


if __name__ == "__main__":
    r = RegionFinder()
