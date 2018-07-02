import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class scanArea(QImage):
    w = 500
    h = 500
    form = 24  # 8-bit grayscale code
    def __init__(self):
        super().__init__(self.w, self.h, self.form)
        self.fill()
