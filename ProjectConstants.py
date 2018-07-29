# To successfully run this application
# download the following: PyQt5, numpy, scipy,
# UniversalPiAPI, spidev (comes with Linux OS)

from PyQt5.QtGui import *

# Size of scan area
defw = 500
defh = 500

# Background Image
IMG = QImage('grid.png')

# Display Thread stats
SAMP_PER_PIX = 1
PIX_PER_UPDATE = 5000
PERIOD_OF_DISP = 500

# Data Thread Stats
FREQ_OF_SAMPLE = 0.01  # in seconds
SAMP_PER_CALL = 500

CALL_PERIOD = 10000000
BETWEEN_TIME = CALL_PERIOD / SAMP_PER_CALL

# Pinouts for Pi
XDAC = 1
YDAC = 2
VADC = 4

# Waveform Frequencies
XHz = 10
YHz = 0.1

# Resolution of generated waveform
waveRes = 1000

# Math Constants
pi = 3.1415926535
bill = 1000000000
