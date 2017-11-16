#! /usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Text(QLineEdit):

    def __init__(self, widget, action):
        super().__init__(widget)
        self.returnPressed.connect(action)
