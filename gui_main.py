#! /usr/bin/python3
import sys
from parsedata import *
from queuesongs import *
from displayqueue import *
from cmuscontrol import *

from gui import *
from gui_table import *
from gui_textbox import *
from gui_button import *
from gui_background import *

class Gui(object):

    def __init__(self, argv):

        self.config = self.initConfig()

        self.app = QApplication(argv)
        self.gui = App()
        self.layout = QVBoxLayout(self.gui)
        self.db = Database()
        self.db.readDatabase('data')

        self.tabs = QTabWidget()
        self.initFirstTab()
        self.initSecondTab()
        self.initThirdTab()
        self.layout.addWidget(self.tabs)
        self.gui.setLayout(self.layout)

        self.gui.initUI()
        sys.exit(self.exitProgram())

    def updateSearch(self):
        query = self.textbox.text()
        self.table.populate(query)

    def setMatch(self, match):
        formatted = "Queue {0}?".format(match['song'])
        buttonReply = QMessageBox.question(self.firstTab, 'Queue Song', formatted, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.qs.queueSong(match)

    def initFirstTab(self):
        self.firstTab = App()
        self.qs = Main(self.config, self.db)

        self.table = Table(self, self.firstTab)
        self.textbox = Text(self.firstTab, self.updateSearch)
        self.button = Button(self.firstTab, 'Search', 'Search the library', self.updateSearch)

        self.table.populate()

        searchbarlayout = QHBoxLayout()
        searchbar = QGroupBox()

        searchbarlayout.addWidget(self.textbox)
        searchbarlayout.addWidget(self.button)
        searchbar.setLayout(searchbarlayout)

        layout = QGridLayout()
        layout.addWidget(searchbar)
        layout.addWidget(self.table, 1, 0)

        self.firstTab.setLayout(layout)
        self.firstTab.initUI()
        self.tabs.addTab(self.firstTab, "Queue Songs")

    def initSecondTab(self):
        self.secondTab = App()
        self.table2 = Table(self, self.secondTab)

        self.dq = Queue(self.config, self.db)

        layout = QGridLayout()
        layout.addWidget(self.table2, 0, 0)

        self.secondTab.setLayout(layout)
        self.secondTab.initUI()
        self.tabs.addTab(self.secondTab, "View Queue")

        self.runnable = Runnable(self.dq)
        QThreadPool.globalInstance().start(self.runnable)

        timer = QTimer(self.secondTab)
        timer.timeout.connect(self.updateSecondTab)
        timer.start(500)

    def initThirdTab(self):
        self.thirdTab = App()

        self.control = Controller(self.config)

        self.playbutton = Button(self.firstTab, 'Play/Pause', 'Start or pause the player', self.control.playpause)
        self.skipbutton = Button(self.firstTab, 'Skip', 'Skip the current song', self.control.skip)
        self.restartbutton = Button(self.firstTab, 'Restart', 'Restart the current song', self.control.restart)

        layout = QGridLayout()
        layout.addWidget(self.restartbutton, 0, 0)
        layout.addWidget(self.playbutton, 0, 1)
        layout.addWidget(self.skipbutton, 0, 2)

        self.thirdTab.setLayout(layout)
        self.thirdTab.initUI()
        self.tabs.addTab(self.thirdTab, "Controls")

    def updateSecondTab(self):
        self.table2.populate(songs=self.runnable.getResult())

    def readConfig(self):
        f = open('config', 'r')
        conflines = f.read().splitlines()
        config = dict([tuple(c.split('=')) for c in conflines])
        f.close()
        return config

    def initConfig(self):
        config = dict()
        if os.path.isfile('config'):
            return self.readConfig()
        else:
            print("No config file found, create a config file and restart!")
            quit()
        if not 'local' in config:
            print("Missing mandatory field local, set local in config and restart!")
            quit()
        elif config['local'].lower() == 'false' and not 'ssh_hostname' in config:
            print("Missing ssh_hostname for remote server, set in config and restart!")
            quit()

    def exitProgram(self):
        self.runnable.stopflag = True
        self.app.exec_()

if __name__ == '__main__':
    Gui(sys.argv)
