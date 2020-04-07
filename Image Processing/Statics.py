import numpy as np
import scipy.ndimage as ndi
import Constants as c


def getIdealGrid(sqh, sqv, numwsquare, numhsquare, angle, tranX, tranY):
    cors = {}
    for i in range(numwsquare):
        for j in range(numhsquare):
            ang = np.deg2rad(angle)
            cors[(i - int(numwsquare / 2), j - int(numhsquare / 2))] = \
                ((i - float(numwsquare - 1) / 2) * sqh * np.cos(ang) + tranX -
                 (j - float(numhsquare - 1) / 2) * sqv * np.sin(ang) + c.img_size / 2,
                 (i - float(numwsquare - 1) / 2) * sqh * np.sin(ang) + tranY +
                 (j - float(numhsquare - 1) / 2) * sqv * np.cos(ang) + c.img_size / 2)
    # print(cors)
    return cors


def distBWPts(c1, c2):
    return np.sqrt(pow(c2[0] - c1[0], 2) + pow(c2[1] - c1[1], 2))


def fill(data, invalid=None):
    if invalid is None:
        invalid = np.isnan(data)
    ind = ndi.distance_transform_edt(invalid, return_distances=False, return_indices=True)
    return data[tuple(ind)]
