#! /usr/bin/python3

import parsedata as pd
import os, sys
import subprocess, shlex

class InitDB(object):

    def __init__(self, database):
        self.db = database
        self.path = None

    def create(self, path):
        self.path = path
        self.createDB()

    def createDB(self):
        # Check whether we have locations, create if not
        string = 'find {0} -name *.mp3'.format(self.path)
        a = subprocess.Popen(shlex.split(string), stdout=subprocess.PIPE)
        res, err = a.communicate()
        res = res.decode('utf-8')
        f = open('locations', 'w')
        f.write(res)
        f.close()
        # Create database
        self.db.writeData('locations', 'data')
        os.remove('locations')

if __name__ == '__main__':
    InitDB()
