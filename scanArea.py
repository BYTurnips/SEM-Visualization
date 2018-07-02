import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class scanArea(QImage):
    def __init__(self):
        super().__init__()
        self.initUI()
