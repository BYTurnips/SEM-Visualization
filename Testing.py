import numpy as np
from scipy.interpolate import UnivariateSpline as UVS
import ProjectConstants as c

LUTX = None
LUTY = None


def generateLUT():
    xcors = mTria(c.waveRes, c.defw)
    xtval = mSawt(c.waveRes, c.bill / c.XHz)
    global LUTX
    LUTX = UVS(xtval, xcors)
    ycors = mSawt(c.waveRes, c.defh)
    ytval = mSawt(c.waveRes, c.bill / c.XHz)
    global LUTY
    LUTY = UVS(ytval, ycors)


def mSine(numS, amp):
    samples = []
    for i in range(numS):
        samples.append((amp / 2 * np.sin((i * 2 * c.pi) / numS) + amp / 2))
    return samples


def mTria(numS, amp):
    samples = []
    for i in range(numS / 4):
        samples.append(amp / 2 + amp * i / (numS * 2))
    for i in range(numS / 2):
        samples.append(amp - amp * i / numS)
    for i in range(numS / 4):
        samples.append(amp * i / (numS * 2))
    return samples


def mSawt(numS, amp):
    samples = []
    for i in range(numS):
        samples.append(amp * i / numS)
    return samples


if __name__ == '__main__':
    # uvs = UVS([0, 1, 2, 3],[1, 2, 3, 4], None, [None, None], 1)
    uvs = generateLUT()
    print(LUTX(1.5))
