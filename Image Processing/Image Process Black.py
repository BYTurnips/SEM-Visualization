# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will track a line of centers, then "straighten" the lines using the average function
# Afterwards, it will take the new lines and arrange them so they closely match a square grid
# with the same rough orientation and size (via average area, average slope of lines)
# this whole transform changes an LUT of each region's upper right corner, and
# linear interpolation is used to transform the image for all future samples.

import numpy as np
import scipy.interpolate as inter
from scipy import ndimage as ndi
import skimage as ski
import skimage.morphology as morph
import skimage.feature as feat
import matplotlib.pyplot as plt
import queue
import copy

squarewidth = 20
squaredist = 5
img_size = 250


class RegionFinder:
    def __init__(self):
        fig, self.axes = plt.subplots(1, 3)
        self.init = ski.io.imread('Cap403.bmp', as_gray=True)

        self.axes[0].imshow(self.init, cmap=plt.cm.gray, interpolation='nearest')

        self.warpcenters = self.findWarpedCenters()
        self.latticecenters = self.labelCenters()

        xs = [x[1] for x in self.warpcenters]
        ys = [x[0] for x in self.warpcenters]
        self.axes[0].scatter(xs, ys, s=10)
        self.axes[2].scatter(xs, ys, s=10)

        self.ideal = self.getIdealGrid(28, 20, 12, 8, 5, -10)
        # self.ideal = self.findGrid()
        xss = [x[1] for x in self.ideal]
        yss = [x[0] for x in self.ideal]
        self.axes[0].scatter(xss, yss, s=10)

        fig, tester = plt.subplots(1, 1)
        tester.imshow(self.init, cmap=plt.cm.gray, interpolation='nearest')
        tester.scatter(xs, ys, s=10)

        # for pt in self.latticecenters:
        #     tester.text(pt[0][1], pt[0][0], pt[1].__repr__(), color='white')

        # the axes get flipped because of weird coordinate shenanigans
        self.luty, self.lutx = self.generateMapping(self.warpcenters, self.ideal)
        self.init = self.convertPicture()
        self.axes[1].imshow(ski.io.imread('whitesq.jpg', as_gray=True), cmap=plt.cm.gray)
        self.axes[1].imshow(self.init, cmap=plt.cm.gray)

        xsss = []
        ysss = []
        for i in range(len(xs)):
            xsss.append(int(xs[i] + self.lutx(xs[i], ys[i])))
            ysss.append(int(ys[i] + self.luty(xs[i], ys[i])))

        self.axes[1].scatter(xsss, ysss, s=10)

        # fig, final = plt.subplots(1, 1)
        # final.imshow(self.init, cmap=plt.cm.gray)

        plt.show()

    def findWarpedCenters(self):
        init = self.init

        edges = feat.canny(init, sigma=3.5)
        edges = morph.dilation(edges)
        filled = ndi.binary_fill_holes(edges)
        filled = morph.erosion(filled)
        filled = morph.remove_small_objects(filled, min_size=70)
        labeled, _ = ndi.label(filled)

        properties = ski.measure.regionprops(labeled)
        centers = []
        avg_area = 0
        for k in properties:
            avg_area += k.area
        avg_area /= len(properties)

        for k in properties:
            if 0.5 < k.area / avg_area < 1.5:
                centers.append(k.centroid)
                newcoords = k.coords
                for q in range(len(k.coords)):
                    newcoords[q][1] = k.coords[q][0]
                    newcoords[q][0] = k.coords[q][1]

        centers = [(round(x), round(y)) for x, y in centers]

        return centers

    def labelCenters(self):
        latticecenters = []
        oorigin = [1000, 1000]
        curmin = 100000000
        for pt in self.warpcenters:
            if self.distBWPts((125, 125), pt) < curmin:
                curmin = self.distBWPts((125, 125), pt)
                oorigin = pt

        print(self.getNeighbors((64, 174)))
        initpt = (oorigin, (0, 0))
        visited = {}
        BFS = queue.Queue()
        BFS.put(initpt)
        count = 0
        # BFS to fill up all the points
        # while BFS.empty() is not True:
        #     pt = BFS.get()
        #     count += 1
        #     # if count % 1 is 0:
        #     #     print(BFS.qsize(), "!", pt[1], "!", end=" ")
        #     if pt[1] in visited:
        #         continue
        #     else:
        #         latticecenters.append(pt)
        #         visited[pt[1]] = True
        #     neighbors = self.getNeighbors(pt[0])
        #     coords = ((0, 1), (-1, 0), (0, -1), (1, 0))
        #     for i in range(4):
        #         newcor = (pt[1][0] + coords[i][0], pt[1][1] + coords[i][1])
        #         if type(neighbors[i]) is not int:
        #             BFS.put((neighbors[i][1], newcor))
        return latticecenters

    def getNeighbors(self, origin):
        # find the 4 closest points to initpt. replace with quickselect alg later
        warp = copy.deepcopy(self.warpcenters)
        closepts = []
        # print(origin)
        for i in range(5):
            curmin = 100000000
            betpt = [1000, 1000]
            for pt in warp:
                if self.distBWPts(origin, pt) < curmin:
                    curmin = self.distBWPts(origin, pt)
                    betpt = pt
            warp.remove(betpt)
            if i is 0:
                continue
            closepts.append(betpt)
        # 2-cos(angle)
        sortedpts = []
        data = []
        for pt in closepts:
            ang = np.arctan2(pt[1] - origin[1], pt[0] - origin[0])
            x = ((ang * 180 / np.pi + 315) % 360, pt)
            data.append(x)

        tryar = [0, 90, 180, 270, 360]
        for i in range(4):
            exist = False
            for pt in data:
                if tryar[i] <= pt[0] <= tryar[i + 1]:
                    exist = True
                    sortedpts.append(pt)
                    break
            if not exist:
                sortedpts.append(-1)
        return sortedpts

    def distBWPts(self, c1, c2):
        return np.sqrt(pow(c2[0] - c1[0], 2) + pow(c2[1] - c1[1], 2))

    def convertPicture(self):
        pic = self.init
        processed = ski.io.imread('whitesq.jpg', as_gray=True)
        self.axes[2].imshow(pic, cmap=plt.cm.gray)
        for i in range(0, 250, 1):
            for j in range(0, 250, 1):
                dx = int(self.lutx(i, j))
                dy = int(self.luty(i, j))
                ix = i - dx
                iy = j - dy
                if 0 <= ix < 250 and 0 <= iy < 250:
                    processed[j][i] = pic[iy][ix]
        return processed

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

    def getIdealGrid(self, sqh, sqv, numsquare, angle, tranX, tranY):
        cors = []
        for i in range(numsquare):
            for j in range(numsquare):
                ang = np.deg2rad(angle)
                cors.append(((i - float(numsquare - 1) / 2) * sqh * np.cos(ang) + tranX -
                             (j - float(numsquare - 1) / 2) * sqv * np.sin(ang) + img_size / 2,
                             (i - float(numsquare - 1) / 2) * sqh * np.sin(ang) + tranY +
                             (j - float(numsquare - 1) / 2) * sqv * np.cos(ang) + img_size / 2))
        return cors

    def fill(self, data, invalid=None):

        if invalid is None:
            invalid = np.isnan(data)

        ind = ndi.distance_transform_edt(invalid, return_distances=False, return_indices=True)
        return data[tuple(ind)]


if __name__ == "__main__":
    g = RegionFinder()
