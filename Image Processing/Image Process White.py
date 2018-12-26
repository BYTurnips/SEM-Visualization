# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will locate every white region and grab the upper-right most point of that region.
# This yields a "grid" of points that is slightly warped.
#
# Alternatively...create a hypothetical grid and do a gradient descent
# on orientation and offset with the cost function testing the sum of the potential energy
# between every warped point and every theoretical point. Potential = -Ae^(-d/t), d is distance
# (might have to change the function though)
#
# This whole transform generates an LUT of each region's centroid, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
from scipy import spatial as spa
from scipy import ndimage as ndi
import skimage as ski
from skimage import morphology
import matplotlib.pyplot as plt

squarewidth = 20
squaredist = 10
img_size = 250


class RegionFinder:
    def __init__(self):
        fig, self.axes = plt.subplots(1, 3, figsize=(8, 3), sharey=True)
        self.init = ski.io.imread('Init_250.bmp', as_gray=True)
        self.warpcenters = self.findWarpedCenters()
        print(self.warpcenters)
        self.findGrid()

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

        self.axes[0].imshow(init, cmap=plt.cm.gray, interpolation='nearest')
        self.axes[0].contour(segmentation, [0.5], linewidths=1.2, colors='y')
        self.axes[1].imshow(image_label_overlay, interpolation='nearest')
        self.axes[2].imshow(init, cmap=plt.cm.gray, interpolation='nearest')

        for a in self.axes:
            a.axis('off')

        for k in properties:
            if 0.5 < k.area / avg_area < 1.5:
                centers.append(k.centroid)
                newcoords = k.coords
                for q in range(len(k.coords)):
                    newcoords[q][1] = k.coords[q][0]
                    newcoords[q][0] = k.coords[q][1]
                # axes[2].add_patch(pat.Polygon(self.minimum_bounding_rectangle(newcoords)))

        centers = [(round(x), round(y)) for x, y in centers]

        xs = [x[1] for x in centers]
        ys = [x[0] for x in centers]
        self.axes[1].scatter(xs, ys)

        return centers

    def findGrid(self):
        width = squarewidth + squaredist
        grid_size = 4
        curmin = 1000000000
        mina = 0
        for a in range(90):
            sumofPE = self.testGridLoss(width, grid_size, a, 0, 0)
            if sumofPE < curmin:
                curmin = sumofPE
                mina = a
                print(curmin)
        # for a in range(4):
        finalideal = self.getIdealGrid(width, grid_size, mina, 0, 0)
        xs = [x[1] for x in finalideal]
        ys = [x[0] for x in finalideal]
        self.axes[0].scatter(xs, ys)

        plt.tight_layout()
        plt.show()

    def testGridLoss(self, sqsize, numsquare, angle, tranX, tranY):
        A = 1
        t = sqsize / 3
        idealgrid = self.getIdealGrid(sqsize, numsquare, angle, tranX, tranY)
        sumofPE = 0
        for i in self.warpcenters:
            for j in idealgrid:
                d = np.sqrt(pow(i[0] - j[0], 2) + pow(i[1] - j[1], 2))
                sumofPE += A * np.exp(-d / t)
                # sumofPE += 1
        return sumofPE

    def getIdealGrid(self, sqsize, numsquare, angle, tranX, tranY):
        cors = []
        for i in range(numsquare):
            for j in range(numsquare):
                # currently rotates about corner point, might change to center of grid
                ang = np.deg2rad(angle)
                cors.append([(i - float(numsquare - 1) / 2) * sqsize * np.cos(ang) + tranX -
                             (j - float(numsquare - 1) / 2) * sqsize * np.sin(ang) + img_size / 2,
                             (i - float(numsquare - 1) / 2) * sqsize * np.sin(ang) + tranY +
                             (j - float(numsquare - 1) / 2) * sqsize * np.cos(ang) + img_size / 2])
        return cors

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

        return rval


if __name__ == "__main__":
    r = RegionFinder()
