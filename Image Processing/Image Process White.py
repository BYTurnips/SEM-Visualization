# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will locate every white region and grab the upper-right most point of that region.
# This yields a "grid" of points that is slightly warped.
#
# A square near the center is chosen, and its 4 nearest neighbors form the basis for the new grid.
# A primitive line tracking algorithm is used to trace each row and column, and the resulting
# lists of IDs corresponding to each row and column gets averaged (LSRL) to find the slope
# these average slopes are averaged across all the lines to yield an orientation.
# With the orientation and the given distances b/w squares and width of squares,
# the new grid lines are repositioned to minimize error.
#
# This whole transform generates an LUT of each region's centroid, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
from scipy import ndimage as ndi
import skimage as ski
from skimage import morphology
import matplotlib.pyplot as plt

squarewidth = 50
squaredist = 20

class RegionFinder:
    def __init__(self):
        self.init = ski.io.imread('Init_250.bmp', as_gray=True)
        self.warpcenters = self.findWarpedCenters()
        print(self.warpcenters)
        self.warplines = self.findLines()

    def findWarpedCenters(self):
        init = self.init
        elevation_map = ski.filters.sobel(init)
        markers = np.zeros_like(init)
        markers[init < 0.1] = 1
        markers[init > 0.9] = 2
        segmentation = morphology.watershed(elevation_map, markers)
        segmentation = ndi.binary_fill_holes(segmentation - 1)
        labeled_init, _ = ndi.label(segmentation)

        properties = ski.measure.regionprops(labeled_init)
        centers = []
        avg_area = 0
        for k in properties:
            avg_area += k.area
        avg_area /= len(properties)
        for k in properties:
            if 0.5 < k.area / avg_area < 1.5:
                centers.append(k.centroid)

        image_label_overlay = ski.color.label2rgb(labeled_init, image=init)

        fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
        axes[0].imshow(init, cmap=plt.cm.gray, interpolation='nearest')
        axes[0].contour(segmentation, [0.5], linewidths=1.2, colors='y')
        axes[1].imshow(image_label_overlay, interpolation='nearest')

        for a in axes:
            a.axis('off')

        centers = [(round(x), round(y)) for x, y in centers]

        xs = [x[1] for x in centers]
        ys = [x[0] for x in centers]
        plt.scatter(xs, ys)

        plt.tight_layout()

        plt.show()

        return centers

    def findLines(self):
        self.warpcenters



if __name__ == "__main__":
    r = RegionFinder()
