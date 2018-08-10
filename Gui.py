# This class generates the responsive UI capabilities of the application

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from QTD_Window import Ui_MainWindow
import ProjectConstants as c
from time import perf_counter


# GUI Class:
# This class creates the actual GUI of the application
# and connects all the signals to their appropriate
# slots in the other threads.
# It gets significant help from the QTD_Window file.
# ...

class GUI(QMainWindow):
    startScanning = pyqtSignal()
    endScanning = pyqtSignal()
    changeXZoom = pyqtSignal(int)
    changeYZoom = pyqtSignal(int)
    newRes = pyqtSignal(int, int)
    sendImage = pyqtSignal(QImage)

    scanPixmap = None
    scanLabel = None


    # Nothing much to say, this creates the UI.
    def __init__(self):
        super().__init__()
        self.scanPixmap = QPixmap()
        self.scanLabel = QLabel('Scan Area', self)

        self.scanLabel.setFixedSize(c.defw, c.defh)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        scanA = c.IMG.copy(0, 0, c.defw, c.defh)
        self.showGivenImage(scanA)
        self.scanLabel.move(300 - c.defw / 2, 320 - c.defh / 2)
        self.scanLabel.show()
        self.connectUI()

    # Connect all the signals and slots
    def connectUI(self):
        self.ui.ScanB.clicked.connect(self.toggleScanning)
        self.ui.RUpdateB.clicked.connect(self.sendRes)
        # self.changeRes()

    # Slot to show the image given by display thread
    def showGivenImage(self, image):
        self.scanLabel.setFixedSize(c.defw, c.defh)
        self.scanPixmap.convertFromImage(image)
        self.scanLabel.setPixmap(self.scanPixmap)
        return

    # Connects Scan button to Main.py's startScanning and endScanning
    def toggleScanning(self, active):
        if active:
            self.startScanning.emit()
        else:
            self.endScanning.emit()

    def sendRes(self):
        neww = self.ui.XRes.value()
        newh = self.ui.YRes.value()
        self.newRes.emit(neww, newh)
