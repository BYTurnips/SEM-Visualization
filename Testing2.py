from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Worker(QThread):
    sendMessage = pyqtSignal(str)

    def __init__(self):
        super()
        QThread.__init__(self)

    def run(self):
        self.sendMessage.emit("HIIIII")
        return


class coolApp(QApplication):
    hireWorker = pyqtSignal()

    def __init__(self):
        super().__init__([])
        self.hireWorker.emit()

    def saystuff(self, message):
        print(message + "!!!")


class Controller:
    def __init__(self):
        app = coolApp()
        app.hireWorker.connect(self.saystuff)
        print("Starting...")
        worker = Worker()
        worker.finished.connect(app.exit)
        worker.sendMessage.connect(app.saystuff)

        worker.start()
        sys.exit(app.exec_())

    def saystuff(self, message):
        print(message)

    def startWorker(self):
        worker2 = Worker()
        worker2.sendMessage.connect(self.saystuff)
        worker2.start()


if __name__ == "__main__":
    c = Controller()