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

# Note: doesn't work on MacOS for some reason, only Windows. Have not tested on Linux.

import numpy as np
import scipy.interpolate as inter
from scipy import ndimage as ndi
import skimage as ski
import skimage.morphology as morph
import matplotlib.pyplot as plt

squarewidth = 20
squaredist = 5
img_size = 250


# rotated, streched, offset grid parameters (close to ideal): (35, 26, 10, 15, 15, 0)

class RegionFinder:
    def __init__(self):
        fig, self.axes = plt.subplots(1, 3)
        self.init = ski.io.imread('Init_250.bmp', as_gray=True)
        self.actinit = self.init

        self.axes[0].imshow(self.init, cmap=plt.cm.gray, interpolation='nearest')

        self.warpcenters = self.findWarpedCenters()
        xs = [x[1] for x in self.warpcenters]
        ys = [x[0] for x in self.warpcenters]
        self.axes[0].scatter(xs, ys, s=10)
        self.axes[2].scatter(xs, ys, s=10)

        self.ideal = self.getIdealGrid(35, 26, 10, 15, 15, 0)
        xss = [x[1] for x in self.ideal]
        yss = [x[0] for x in self.ideal]
        self.axes[0].scatter(xss, yss, s=10)

        # the axes get flipped because of weird coordinate shenanigans
        self.luty, self.lutx = self.generateMapping(self.warpcenters, self.ideal)
        self.init = self.convertPicture()
        # self.axes[1].imshow(ski.io.imread('whitesq.jpg', as_gray=True), cmap=plt.cm.gray)
        self.axes[1].imshow(self.init, cmap=plt.cm.gray)

        xsss = []
        ysss = []
        newb = []
        for i in range(len(xs)):
            xsss.append(int(xs[i] + self.lutx(xs[i], ys[i])))
            ysss.append(int(ys[i] + self.luty(xs[i], ys[i])))
            newb.append(int(self.actinit[int(xs[i]), int(ys[i])]))

        self.axes[1].scatter(xsss, ysss, s=10)

        parray = np.column_stack((xs, ys, xsss, ysss, newb))
        print(parray)

        # self.warpcenters = self.findWarpedCenters()
        # xs = [x[1] for x in self.warpcenters]
        # ys = [x[0] for x in self.warpcenters]
        # self.axes[1].scatter(xs, ys, s=10)

        plt.show()

    def findWarpedCenters(self):
        init = self.init
        elevation_map = ski.filters.sobel(init)
        markers = np.zeros_like(init)
        markers[init < 0.1] = 1
        markers[init > 0.9] = 2
        segmentation = morph.watershed(elevation_map, markers)
        segmentation = ndi.binary_fill_holes(segmentation - 1)
        labeled_init, _ = ndi.label(segmentation)

        properties = ski.measure.regionprops(labeled_init)
        centers = []
        avg_area = 0
        for k in properties:
            avg_area += k.area
        avg_area /= len(properties)

        # image_label_overlay = ski.color.label2rgb(labeled_init, image=init)

        # self.axes[0].imshow(init, cmap=plt.cm.gray, interpolation='nearest')
        # self.axes[0].contour(segmentation, [0.5], linewidths=1.2, colors='y')
        # self.axes[1].imshow(image_label_overlay, interpolation='nearest')

        for k in properties:
            if 0.5 < k.area / avg_area < 1.5:
                centers.append(k.centroid)
                newcoords = k.coords
                for q in range(len(k.coords)):
                    newcoords[q][1] = k.coords[q][0]
                    newcoords[q][0] = k.coords[q][1]

        centers = [(round(x), round(y)) for x, y in centers]

        return centers

    def findGrid(self):
        w = squarewidth + squaredist
        h = squarewidth + squaredist
        size = 12
        curmin = 1000000000
        ares = 18
        tres = 5
        mina, minx, miny = 0, 0, 0
        for a in range(ares):
            print(a)
            for x in range(tres):
                for y in range(tres):
                    A = 90 * a / ares
                    X = w * x / tres
                    Y = w * y / tres
                    sumofPE = self.testGridLoss(w, h, size, A, X, Y)
                    if sumofPE < curmin:
                        curmin = sumofPE
                        mina = a
                        minx = x
                        miny = y
                        print(curmin, minx, miny)
        finalideal = self.getIdealGrid(w, h, size, mina, w * minx / tres, w * miny / tres)

        return finalideal

    def testGridLoss(self, sqh, sqv, numsquare, angle, tranX, tranY):
        t = (squarewidth + squaredist) / 3
        idealgrid = self.getIdealGrid(sqh, sqv, numsquare, angle, tranX, tranY)
        sumofPE = 0
        for i in self.warpcenters:
            for j in idealgrid:
                d = np.sqrt(pow(i[0] - j[0], 2) + pow(i[1] - j[1], 2))
                sumofPE += -10 * np.exp(-d / t)
        return sumofPE

    def generateMapping(self, warped, ideal):
        # currently closest-neighbor method mapping
        x, y, dx, dy = [], [], [], []
        for warp in warped:
            close = [1000, 1000]
            curmin = 100000000
            for ipt in ideal:
                if self.distBWPts(ipt, warp) < curmin:
                    curmin = self.distBWPts(ipt, warp)
                    close = ipt
            # dest =
            x.append(warp[0])
            y.append(warp[1])
            dx.append(close[0] - warp[0])
            dy.append(close[1] - warp[1])

        x = np.asarray(x)
        y = np.asarray(y)
        dx = np.asarray(dx)
        dy = np.asarray(dy)
        coors = np.column_stack((x, y))

        res = 50

        rows = np.arange(0, 251, 250 / res)
        cols = np.arange(0, 251, 250 / res)

        grid_x, grid_y = np.mgrid[0:250:complex(0, res + 1), 0:250:complex(0, res + 1)]

        tlutx = inter.griddata(coors, dx, (grid_x, grid_y))
        tluty = inter.griddata(coors, dy, (grid_x, grid_y))
        tlutx = self.fill(tlutx)
        tluty = self.fill(tluty)
        lutx = inter.interp2d(rows, cols, tlutx)
        luty = inter.interp2d(rows, cols, tluty)

        return lutx, luty

    def convertPicture(self):
        # pic = ski.io.imread('gradientgray.jpg', as_gray=True)
        pic = self.init
        processed = ski.io.imread('whitesq.jpg', as_gray=True)
        self.axes[2].imshow(pic, cmap=plt.cm.gray)
        for i in range(0, 250, 1):
            for j in range(0, 250, 1):
                dx = int(self.lutx(i, j))
                dy = int(self.luty(i, j))
                ix = i - dx
                iy = j - dy
                if i == 14 and j == 79:
                    print(ix, iy)
                    self.axes[1].arrow(ix, iy, dx, dy, head_width=4)
                    self.axes[2].arrow(ix, iy, dx, dy, head_width=4)
                if 0 <= ix < 250 and 0 <= iy < 250:
                    processed[j][i] = pic[iy][ix]
                if i % 25 == 0 and j % 25 == 0:
                    self.axes[1].arrow(ix, iy, dx, dy, head_width=4)
                    self.axes[2].arrow(ix, iy, dx, dy, head_width=4)
        return processed

    def gridGradDesc(self):
        w = squarewidth + squaredist
        size = 10
        A = 0
        X = 0
        Y = 0
        alearn = 0.01
        xylearn = 0.01

        for cycle in range(100):
            # Finding the initial loss
            init_loss = self.testGridLoss(w, size, A, X, Y)
            self.ergraph.scatter(cycle, init_loss, s=10)
            # Finding the partial derivatives aka the gradient
            dA = (self.testGridLoss(w, size, A + 0.000001, X, Y) - init_loss) / 0.000001
            dX = (self.testGridLoss(w, size, A, X + 0.000001, Y) - init_loss) / 0.000001
            dY = (self.testGridLoss(w, size, A, X, Y + 0.000001) - init_loss) / 0.000001

            print(round(A, 3), round(X, 3), round(Y, 3), round(init_loss, 3), "D/DL",
                  round(dA, 3), round(dX, 3), round(dY, 3))

            A -= alearn * dA
            X -= xylearn * dX
            Y -= xylearn * dY

        finalideal = self.getIdealGrid(w, size, A, X, Y)
        xs = [x[1] for x in finalideal]
        ys = [x[0] for x in finalideal]
        self.axes[0].scatter(xs, ys, s=10)
        self.axes[2].scatter(xs, ys, s=10)

        plt.tight_layout()
        plt.show()

        return finalideal

    def distBWPts(self, c1, c2):
        return np.sqrt(pow(c2[0] - c1[0], 2) + pow(c2[1] - c1[1], 2))

    def getIdealGrid(self, sqh, sqv, numsquare, angle, tranX, tranY):
        cors = []
        for i in range(numsquare):
            for j in range(numsquare):
                ang = np.deg2rad(angle)
                cors.append([(i - float(numsquare - 1) / 2) * sqh * np.cos(ang) + tranX -
                             (j - float(numsquare - 1) / 2) * sqv * np.sin(ang) + img_size / 2,
                             (i - float(numsquare - 1) / 2) * sqh * np.sin(ang) + tranY +
                             (j - float(numsquare - 1) / 2) * sqv * np.cos(ang) + img_size / 2])
        return cors

    def fill(self, data, invalid=None):

        if invalid is None:
            invalid = np.isnan(data)

        ind = ndi.distance_transform_edt(invalid, return_distances=False, return_indices=True)
        return data[tuple(ind)]


if __name__ == "__main__":
    r = RegionFinder()
