import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import hough_line
from skimage.io import imread
from skimage.util import invert
from skimage import morphology as morph
from skimage.feature import canny

inv = imread('Init_250.bmp', as_gray=True)
inv = invert(inv)
inv = morph.erosion(inv, selem=np.ones((3, 3)))
inv = canny(inv)

img = inv

out, angles, d = hough_line(img)

fix, axes = plt.subplots(1, 2, figsize=(7, 4))

axes[0].imshow(img, cmap=plt.cm.gray)
axes[0].set_title('Input image')

axes[1].imshow(
    out, cmap=plt.cm.bone,
    extent=(np.rad2deg(angles[-1]),
            np.rad2deg(angles[0]), d[-1], d[0]))
axes[1].set_title('Hough transform')
axes[1].set_xlabel('Angle (degree)')
axes[1].set_ylabel('Distance (pixel)')

plt.tight_layout()
plt.show()
