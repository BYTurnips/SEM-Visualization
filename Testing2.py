from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Worker(QThread):
    sendMessage = pyqtSignal(str)

    def __init__(self):
        super()
        QThread.__init__(self)
        # self.sendMessage = pyqtSignal(str)

    def run(self):
        self.sendMessage.emit("HIIIII")
        return


class Controller():
    def __init__(self):
        app = QCoreApplication([])
        print("Starting...")
        worker = Worker()
        worker.finished.connect(app.exit)
        worker.sendMessage.connect(self.saystuff)
        worker.start()
        sys.exit(app.exec_())

    def saystuff(self, message):
        print(message)


if __name__ == "__main__":
    c = Controller()

# import sys
# import time
#
# from PyQt5.QtCore import *
#
#
# # Subclassing QThread
# # http://qt-project.org/doc/latest/qthread.html
# class AThread(QThread):
#
#     def run(self):
#         count = 0
#         while count < 5:
#             time.sleep(1)
#             print("A Increasing")
#             count += 1
#
#
# class Controller:
#     def __init__(self):
#         self.using_q_thread()
#
#     def using_q_thread(self):
#         app = QCoreApplication([])
#         thread = AThread()
#         thread.finished.connect(app.exit)
#         thread.start()
#         sys.exit(app.exec_())
#
#
# if __name__ == "__main__":
#     c = Controller()
