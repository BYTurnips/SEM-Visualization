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
        # Grid Properties (actual size is 11 x 8)
        self.ysize = 16
        self.xsize = 16
        self.vsize = 25
        self.wsize = 25

        fig, self.axes = plt.subplots(1, 3)
        self.init = ski.io.imread('Init_250.bmp', as_gray=True)

        self.axes[0].imshow(self.init, cmap=plt.cm.gray, interpolation='nearest')

        self.warpcenters = self.findWarpedCenters()
        self.latticecenters = self.labelCenters()
        print(self.latticecenters)

        xs = [x[1] for x in self.warpcenters]
        ys = [x[0] for x in self.warpcenters]
        self.axes[0].scatter(xs, ys, s=10)
        self.axes[2].scatter(xs, ys, s=10)

        self.ideal = self.getIdealGrid(self.vsize, self.wsize, self.xsize, self.ysize, 0, 0, 0)
        xss = [x[1] for x in self.ideal.values()]
        yss = [x[0] for x in self.ideal.values()]
        self.axes[0].scatter(xss, yss, s=10)

        fig, tester = plt.subplots(1, 1)
        tester.imshow(self.init, cmap=plt.cm.gray, interpolation='nearest')
        tester.scatter(xs, ys, s=10)

        for pt in self.latticecenters:
            tester.text(pt[0][1], pt[0][0], pt[1].__repr__(), color='white')

        # the axes get flipped because of weird coordinate shenanigans
        self.luty, self.lutx = self.generateMapping(self.latticecenters, self.ideal)
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

        initpt = (oorigin, (0, 0))
        visited = {}
        BFS = queue.Queue()
        BFS.put(initpt)
        count = 0
        # BFS to fill up all the points
        while BFS.empty() is not True:
            pt = BFS.get()
            count += 1
            if pt[1] in visited:
                continue
            else:
                latticecenters.append(pt)
                visited[pt[1]] = True
            neighbors = self.getNeighbors(pt[0])
            coords = ((0, 1), (-1, 0), (0, -1), (1, 0))
            for i in range(4):
                newcor = (pt[1][0] + coords[i][0], pt[1][1] + coords[i][1])
                if type(neighbors[i]) is not int:
                    BFS.put((neighbors[i][1], newcor))
        return latticecenters

    def getNeighbors(self, origin):
        narrow_amt = (np.pi / 180) * 30
        # find the 4 closest points to initpt. replace with quickselect alg later
        warp = copy.deepcopy(self.warpcenters)
        closepts = []
        for i in range(9):
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

        data = []
        for pt in closepts:
            # more coordinate shenanigans
            ang = np.arctan2(origin[0] - pt[0], pt[1] - origin[1])
            x = [(ang + 2 * np.pi) % (2 * np.pi), pt]
            data.append(x)

        sortedpts = []
        tryar = [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
        for i in range(4):
            curmin = 100000000
            betpt = [-1, -1]
            for pt in data:
                multiplier = pow((2 - np.cos(pt[0] - tryar[i])), 2)
                score = self.distBWPts(origin, pt[1]) * multiplier
                if score < curmin:
                    curmin = score
                    betpt = pt
            # it's possible that it should be more complex than betpt[0]+np.pi/4
            # it's possible that this thing doesn't wrap around at 360 deg
            if tryar[i] + narrow_amt <= betpt[0] + np.pi / 4 <= tryar[i + 1] - narrow_amt:
                sortedpts.append(betpt)
            else:
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
            x.append(warp[0][0])
            y.append(warp[0][1])
            print(ideal)
            dx.append(ideal[(warp[1][0], warp[1][1])][0] - warp[0][0])
            dy.append(ideal[(warp[1][0], warp[1][1])][1] - warp[0][1])

        x = np.asarray(x)
        y = np.asarray(y)
        coors = np.column_stack((x, y))
        dx = np.asarray(dx)
        dy = np.asarray(dy)


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

    def getIdealGrid(self, sqh, sqv, numwsquare, numhsquare, angle, tranX, tranY):
        cors = {}
        for i in range(numwsquare):
            for j in range(numhsquare):
                ang = np.deg2rad(angle)
                cors[(i - numwsquare / 2, j - numhsquare / 2)] = \
                    (((i - float(numwsquare - 1) / 2) * sqh * np.cos(ang) + tranX -
                      (j - float(numhsquare - 1) / 2) * sqv * np.sin(ang) + img_size / 2,
                      (i - float(numwsquare - 1) / 2) * sqh * np.sin(ang) + tranY +
                      (j - float(numhsquare - 1) / 2) * sqv * np.cos(ang) + img_size / 2))
        return cors

    def fill(self, data, invalid=None):

        if invalid is None:
            invalid = np.isnan(data)

        ind = ndi.distance_transform_edt(invalid, return_distances=False, return_indices=True)
        return data[tuple(ind)]


if __name__ == "__main__":
    g = RegionFinder()
