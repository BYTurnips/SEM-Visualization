import queue
import copy
import matplotlib.pyplot as plt
import scipy.interpolate as inter
import scipy.ndimage as ndi
import skimage.measure as meas
import skimage.morphology as morph
import skimage.feature as feat
import skimage.io as skiio
import numpy as np

# IMAGE PARAMETERS
img = skiio.imread('Cap403border.png', as_gray=True)
timg = skiio.imread('fewsquares.png', as_gray=True)
whitesq = skiio.imread('whitesq.jpg', as_gray=True)
img_size = 250

# IDEAL GRID PARAMETERS
# x, y size = # cells in each direction
# v, w size = size of individual cells
# Test Grid dimensions: 11 x 8
ysize = 15
xsize = ysize
vsize = 25
wsize = 25

# LINE FINDING PARAMETERS
anglvl = (np.pi / 180) * 30

# LUT GENERATION PARAMETERS
res = 50
