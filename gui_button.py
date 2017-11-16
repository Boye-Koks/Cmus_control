#! /usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Button(QPushButton):

    def __init__(self, widget, name, tooltip, action):
        super().__init__(name, widget)
        self.setToolTip(tooltip)
        self.clicked.connect(action)
