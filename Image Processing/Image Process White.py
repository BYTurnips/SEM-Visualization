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
# Alternatively...create a hypothetical grid and do a binary search or gradient descent
# on orientation and offset with the function testing the sum of the least square error
# between the hypothetical grid and the real grid.
#
# This whole transform generates an LUT of each region's centroid, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
from scipy import spatial as spa
from scipy import ndimage as ndi
import skimage as ski
from skimage import morphology
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import cv2 as cv

squarewidth = 50
squaredist = 20

class RegionFinder:
    def __init__(self):
        self.init = ski.io.imread('Init_250.bmp', as_gray=True)
        self.warpcenters = self.findWarpedCenters()
        print(self.warpcenters)


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


        image_label_overlay = ski.color.label2rgb(labeled_init, image=init)

        fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharey=True)
        axes[0].imshow(init, cmap=plt.cm.gray, interpolation='nearest')
        axes[0].contour(segmentation, [0.5], linewidths=1.2, colors='y')
        axes[1].imshow(image_label_overlay, interpolation='nearest')

        for a in axes:
            a.axis('off')

        for k in properties:
            if 0.5 < k.area / avg_area < 1.5:
                centers.append(k.centroid)
                # t = k.coords[1]
                # k.coords[1] = k.coords[0]
                # k.coords[0] = t
                newcoords = k.coords
                for q in range(len(k.coords)):
                    newcoords[q][1] = k.coords[q][0]
                    newcoords[q][0] = k.coords[q][1]
                axes[0].add_patch(pat.Polygon(self.minimum_bounding_rectangle(newcoords)))

        centers = [(round(x), round(y)) for x, y in centers]

        xs = [x[1] for x in centers]
        ys = [x[0] for x in centers]
        axes[1].scatter(xs, ys)

        # for k in properties:
        #     axes[2].add_patch(pat.Polygon(self.minimum_bounding_rectangle(k.coords)))

        plt.tight_layout()
        plt.show()

        return centers

    def findLines(self):
        cstart = self.warpcenters[1]
        cv.min
        # for k in self.warpcenters:
        #     if (abs(k[1]-125)+abs(k[0]-125)) <

    def minimum_bounding_rectangle(self, points):
        """
        Find the smallest bounding rectangle for a set of points.
        Returns a set of points representing the corners of the bounding box.

        :param points: an nx2 matrix of coordinates
        :rval: an nx2 matrix of coordinates
        """
        from scipy.ndimage.interpolation import rotate
        pi2 = np.pi / 2.

        # get the convex hull for the points
        hull_points = points[spa.ConvexHull(points).vertices]

        # calculate edge angles
        edges = np.zeros((len(hull_points) - 1, 2))
        edges = hull_points[1:] - hull_points[:-1]

        angles = np.zeros((len(edges)))
        angles = np.arctan2(edges[:, 1], edges[:, 0])

        angles = np.abs(np.mod(angles, pi2))
        angles = np.unique(angles)

        # find rotation matrices
        # XXX both work
        rotations = np.vstack([
            np.cos(angles),
            np.cos(angles - pi2),
            np.cos(angles + pi2),
            np.cos(angles)]).T
        #     rotations = np.vstack([
        #         np.cos(angles),
        #         -np.sin(angles),
        #         np.sin(angles),
        #         np.cos(angles)]).T
        rotations = rotations.reshape((-1, 2, 2))

        # apply rotations to the hull
        rot_points = np.dot(rotations, hull_points.T)

        # find the bounding points
        min_x = np.nanmin(rot_points[:, 0], axis=1)
        max_x = np.nanmax(rot_points[:, 0], axis=1)
        min_y = np.nanmin(rot_points[:, 1], axis=1)
        max_y = np.nanmax(rot_points[:, 1], axis=1)

        # find the box with the best area
        areas = (max_x - min_x) * (max_y - min_y)
        best_idx = np.argmin(areas)

        # return the best box
        x1 = max_x[best_idx]
        x2 = min_x[best_idx]
        y1 = max_y[best_idx]
        y2 = min_y[best_idx]
        r = rotations[best_idx]

        rval = np.zeros((4, 2))
        rval[0] = np.dot([x1, y2], r)
        rval[1] = np.dot([x2, y2], r)
        rval[2] = np.dot([x2, y1], r)
        rval[3] = np.dot([x1, y1], r)
        # rval[0] = np.dot([y2, x1], r)
        # rval[1] = np.dot([y2, x2], r)
        # rval[2] = np.dot([y1, x2], r)
        # rval[3] = np.dot([y1, x1], r)

        return rval



if __name__ == "__main__":
    r = RegionFinder()
