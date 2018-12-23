# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will locate every line, then "straighten" the lines using the average function
# Afterwards, it will take the new lines and arrange them so they closely match a square grid
# with the same rough orientation and size (via average area, average slope of lines)
# this whole transform changes an LUT of each region's upper right corner, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
import scipy as sp
import skimage as scikit

LUT = [[1, 2],
       [2, 1]]

if __name__ == "__main__":
