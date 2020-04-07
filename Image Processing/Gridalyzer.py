import numpy as np
import scipy.ndimage as ndi
import skimage.measure as meas
import skimage.morphology as morph
import skimage.feature as feat
import queue
import copy
import Statics as f
import Constants as c


def findWarpedCenters(img):
    edges = feat.canny(img, sigma=3.5)
    edges = morph.dilation(edges)
    filled = ndi.binary_fill_holes(edges)
    filled = morph.erosion(filled)
    filled = morph.remove_small_objects(filled, min_size=70)
    labeled, _ = ndi.label(filled)

    properties = meas.regionprops(labeled)
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


def labelCenters(warpcenters, img_size):
    midpoint = (img_size / 2, img_size / 2)
    latticecenters = []
    oorigin = None
    curmin = float("inf")
    for pt in warpcenters:
        if f.distBWPts(midpoint, pt) < curmin:
            curmin = f.distBWPts(midpoint, pt)
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
        neighbors = getNeighbors(pt[0], warpcenters)
        coords = ((0, 1), (-1, 0), (0, -1), (1, 0))
        for i in range(4):
            newcor = (pt[1][0] + coords[i][0], pt[1][1] + coords[i][1])
            if type(neighbors[i]) is not int:
                BFS.put((neighbors[i][1], newcor))
    return latticecenters


# This function is the most disgustingly inefficient thing ever, probably needs fixing
def getNeighbors(origin, warpcenters):
    # find the 9 closest points to initpt. replace with quickselect alg later
    warp = copy.deepcopy(warpcenters)
    closepts = []
    for i in range(min(9, len(warp))):
        curmin = float("inf")
        betpt = None
        for pt in warp:
            if f.distBWPts(origin, pt) < curmin:
                curmin = f.distBWPts(origin, pt)
                betpt = pt
        warp.remove(betpt)
        if i is 0:
            continue
        closepts.append(betpt)

    data = []
    for pt in closepts:
        # coordinate shenanigans
        ang = np.arctan2(origin[0] - pt[0], pt[1] - origin[1])
        x = [(ang + 2 * np.pi) % (2 * np.pi), pt]
        data.append(x)

    sortedpts = []
    tryar = [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
    for i in range(4):
        curmin = float("inf")
        betpt = None
        for pt in data:
            multiplier = pow((2 - np.cos(pt[0] - tryar[i])), 2)
            score = f.distBWPts(origin, pt[1]) * multiplier
            if score < curmin:
                curmin = score
                betpt = pt
        # it's possible that it should be more complex than betpt[0]+np.pi/4
        # it's possible that this thing doesn't wrap around at 360 deg
        if tryar[i] + c.anglvl <= betpt[0] + np.pi / 4 <= tryar[i + 1] - c.anglvl:
            sortedpts.append(betpt)
        else:
            sortedpts.append(-1)
    return sortedpts
