# The program will take in a slightly warped grid and output a true grid by remapping every point.
# It will track a line of centers, then "straighten" the lines using the average function
# Afterwards, it will take the new lines and arrange them so they closely match a square grid
# with the same rough orientation and size (via average area, average slope of lines)
# this whole transform changes an LUT of each region's upper right corner, and
# linear interpolation is used to transform the image for all future samples.
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as inter
import skimage.morphology as morph

import Constants as c
import Statics as f
import Gridalyzer as g

class RegionFinder:
    def __init__(self):
        self.init = c.timg
        self.final = c.timg
        self.warpcenters = None
        self.latticecenters = None

        self.warpcenters = g.findWarpedCenters(self.init)
        self.latticecenters = g.labelCenters(self.warpcenters, c.img_size)
        self.ideal = f.getIdealGrid(c.vsize, c.wsize, c.xsize, c.ysize, 0, 0, 0)
        self.luty, self.lutx = self.generateMapping(self.latticecenters, self.ideal)
        self.final = self.convertPicture()
        self.final = morph.opening(self.final)

        self.printResults()

    def printResults(self):
        xwarpcor = [x[1] for x in self.warpcenters]
        ywarpcor = [x[0] for x in self.warpcenters]
        xidealcor = [x[1] for x in self.ideal.values()]
        yidealcor = [x[0] for x in self.ideal.values()]

        fig, axes = plt.subplots(1, 2)

        # Initial + Ideal end position
        axes[0].imshow(self.init, cmap='gray', interpolation='nearest')
        axes[0].scatter(xwarpcor, ywarpcor, s=10)
        axes[0].scatter(xidealcor, yidealcor, s=10)

        # Result of conversion, and independently calculated centroid transformation
        axes[1].imshow(c.whitesq, cmap='gray')
        axes[1].imshow(self.final, cmap='gray')
        xtranscor = []
        ytranscor = []
        for i in range(len(xwarpcor)):
            xtranscor.append(int(xwarpcor[i] + self.luty(xwarpcor[i], ywarpcor[i])))
            ytranscor.append(int(ywarpcor[i] + self.lutx(xwarpcor[i], ywarpcor[i])))
        axes[1].scatter(xtranscor, ytranscor, s=10)

        # Unused at the moment
        # axes[2].imshow(self.init, cmap='gray')
        # axes[2].scatter(xwarpcor, ywarpcor, s=10)

        # fig, tester = plt.subplots(1, 1)
        # tester.imshow(self.init, cmap='gray, interpolation='nearest')
        # tester.scatter(xwarpcor, ywarpcor, s=10)
        #
        # for pt in self.latticecenters:
        #     tester.text(pt[0][1], pt[0][0], pt[1].__repr__(), color='black')

        plt.show()

    def convertPicture(self):
        pic = self.init
        processed = c.whitesq
        for x in range(0, c.img_size, 1):
            for y in range(0, c.img_size, 1):
                ix = x + int(self.luty(x, y))
                iy = y + int(self.lutx(x, y))
                if 0 <= ix < c.img_size and 0 <= iy < c.img_size:
                    processed[iy][ix] = pic[y][x]
        return processed

    def generateMapping(self, warped, ideal):
        x, y, dx, dy = [], [], [], []

        # From here on: (x,y) represents coordinates as seen on the plotting
        for warp in warped:
            x.append(warp[0][1])
            y.append(warp[0][0])
            dx.append(ideal[(warp[1][0], warp[1][1])][1] - warp[0][1])
            dy.append(ideal[(warp[1][0], warp[1][1])][0] - warp[0][0])

        dx = np.asarray(dx)
        dy = np.asarray(dy)
        coors = np.column_stack((np.asarray(y), np.asarray(x)))

        gl = np.arange(0, c.img_size + 1, c.img_size / c.res)
        grid_x, grid_y = np.mgrid[0:c.img_size:complex(0, c.res + 1), 0:c.img_size:complex(0, c.res + 1)]

        # may want to use rectbivariatespline
        lutx = inter.interp2d(gl, gl, f.fill(inter.griddata(coors, dx, (grid_x, grid_y))))
        luty = inter.interp2d(gl, gl, f.fill(inter.griddata(coors, dy, (grid_x, grid_y))))

        return lutx, luty


if __name__ == "__main__":
    g = RegionFinder()
