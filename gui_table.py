#! /usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Table(QTableWidget):

    def __init__(self, widget, tab):
        super().__init__(tab)
        self.db = widget.db
        self.widget = widget

        self.doubleClicked.connect(self.table_click)

        self.matches = list()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels("Artist;Song".split(";"))

    def populate(self, matchstring=None, songs=None):
        if not songs:
            self.matches = self.db.findMatches(matchstring)
        elif songs[0] == -1:
            self.matches = []
        else:
            self.matches = songs
        self.setRowCount(len(self.matches))
        i = 0
        for match in self.matches:
            self.setItem(i, 0, QTableWidgetItem(match['artist']))
            self.setItem(i, 1, QTableWidgetItem(match['song']))
            i += 1
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)


    def table_click(self):
        selectedItem = self.selectedItems()[0]
        row = selectedItem.row()
        # song_hash = hash(self.matches[row]['location'])
        self.widget.setMatch(self.matches[row])
