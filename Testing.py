import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import *


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QLabel(self)
        image = QImage(100, 100, 24)
        image.load('Yellow_BG.JPG')

        paint = QPainter()
        paint.begin(image)
        paint.drawRect(20, 20, 20, 20)
        paint.end()
        # pixmap = QPixmap('Cool Logo.jpg')
        pixmap = QPixmap()
        pixmap.convertFromImage(image)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())