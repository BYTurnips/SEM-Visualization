from PyQt5.QtGui import *

defw = 500
defh = 500

SAMP_PER_PIX = 1

SAMP_PER_CALL = 25000
FREQ_OF_CALL = 100
CALL_PERIOD = 10000000

IMG = QImage('grid.png')

XDAC = 1
YDAC = 2
VADC = 4

XHz = 10
YHz = 0.1

waveRes = 1000

pi = 3.1415926535

# def initConstants():
#     globals().IMG = globals().IMG.copy(0, 0, defw, defh)
