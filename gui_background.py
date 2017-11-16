#! /usr/bin/python3

import time
from PyQt5.QtCore import *

class Runnable(QRunnable):

    def __init__(self, dq):
        super().__init__()
        self.dq = dq
        self.result = None
        self.stopflag = False

    def run(self):
        app = QCoreApplication.instance()
        while True:
            self.result = self.dq.show()
            print("Running!")
            time.sleep(1)
        app.quit()

    def getResult(self):
        return self.result
