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
        fig, self.axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
        fig, self.ergraph = plt.subplots(1, 1, figsize=(8, 3), sharey=True)
        self.init = ski.io.imread('Init_250.bmp', as_gray=True)
        self.warpcenters = self.findWarpedCenters()
        self.gridGradDesc()

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
        # self.axes[2].imshow(init, cmap=plt.cm.gray, interpolation='nearest')

        # for a in self.axes:
        #     a.axis('off')

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
        grid_size = 12
        curmin = 1000000000
        ares = 90
        tres = 5
        mina = 0
        minx = 0
        miny = 0
        for a in range(ares):
            sumofPE = self.testGridLoss(width, grid_size, 90 * a / ares, 0, 0)
            if sumofPE < curmin:
                curmin = sumofPE
                mina = a
                # print(curmin)

        for x in range(tres):
            for y in range(tres):
                sumofPE = self.testGridLoss(width, grid_size, mina, width * x / tres, width * y / tres)
                if sumofPE < curmin:
                    curmin = sumofPE
                    minx = x
                    miny = y
                    print(curmin, minx, miny)
        minx = 0
        miny = 0
        finalideal = self.getIdealGrid(width, grid_size, mina, width * minx / tres, width * miny / tres)
        xs = [x[1] for x in finalideal]
        ys = [x[0] for x in finalideal]
        self.axes[0].scatter(xs, ys, s=10)

        plt.tight_layout()
        plt.show()

    def gridGradDesc(self):
        width = squarewidth + squaredist
        grid_size = 10
        mina = 0
        A = 0
        X = 0
        Y = 0
        learn = 0.5

        for cycle in range(40):
            # Finding the initial loss
            init_loss = self.testGridLoss(width, grid_size, A, X, Y)
            self.ergraph.scatter(cycle, init_loss, s=10)
            # Finding the partial derivatives aka the gradient
            dA = (self.testGridLoss(width, grid_size, A + 0.0001, X, Y) - init_loss) / 0.0001
            dX = (self.testGridLoss(width, grid_size, A, X + 0.0001, Y) - init_loss) / 0.0001
            dY = (self.testGridLoss(width, grid_size, A, X, Y + 0.0001) - init_loss) / 0.0001

            print(round(A, 3), round(X, 3), round(Y, 3), round(init_loss, 3), "D/DL",
                  round(dA, 3), round(dX, 3), round(dY, 3))

            A -= learn * dA
            X -= learn * dX
            Y -= learn * dY

        finalideal = self.getIdealGrid(width, grid_size, A, X, Y)
        xs = [x[1] for x in finalideal]
        ys = [x[0] for x in finalideal]
        self.axes[0].scatter(xs, ys, s=10)

        plt.tight_layout()
        plt.show()

    def testGridLoss(self, sqsize, numsquare, angle, tranX, tranY):
        t = sqsize / 3
        idealgrid = self.getIdealGrid(sqsize, numsquare, angle, tranX, tranY)
        sumofPE = 0
        for i in self.warpcenters:
            for j in idealgrid:
                d = np.sqrt(pow(i[0] - j[0], 2) + pow(i[1] - j[1], 2))
                sumofPE += 10 * np.exp(-d / t)
                # sumofPE += pow(d, 2)/5000
        return sumofPE

    def getIdealGrid(self, sqsize, numsquare, angle, tranX, tranY):
        cors = []
        for i in range(numsquare):
            for j in range(numsquare):
                ang = np.deg2rad(angle)
                cors.append([(i - float(numsquare - 1) / 2) * sqsize * np.cos(ang) + tranX -
                             (j - float(numsquare - 1) / 2) * sqsize * np.sin(ang) + img_size / 2,
                             (i - float(numsquare - 1) / 2) * sqsize * np.sin(ang) + tranY +
                             (j - float(numsquare - 1) / 2) * sqsize * np.cos(ang) + img_size / 2])
        return cors


if __name__ == "__main__":
    r = RegionFinder()
