import sys
from PyQt5.QtWidgets import *
from QTD_Window import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())

# cd Documents/Extracurricular/'Science Research'/Pease_AWESem/SEM-Visualization
# pyuic5 -x mainwindow.ui -o QTD_Conv.py
