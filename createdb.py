#! /usr/bin/python3

import os, sys
import subprocess, shlex
from mutagen.mp3 import HeaderNotFoundError
from mutagen.mp3 import EasyMP3 as mp3
from progress.bar import Bar

class InitDB(object):

    def __init__(self):
        locations = self.getLocations()
        datafile = self.initFile()
        bar = Bar('Processing', max=(len(locations)))
        errorfile = open('errors', 'w')
        for location in locations:
            try:
                artist, song = self.toDict(location)
                line = "{0} | {1} | {2}\n".format(artist, song, location)
                datafile.write(line)
            except (KeyError, HeaderNotFoundError):
                errorfile.write(location)
            bar.next()
        datafile.close()
        errorfile.close()
        bar.finish()

    def initFile(self):
        datafile = open('data', 'w')
        datafile.write('')
        datafile.close()
        return open('data', 'a')

    def getLocations(self):
        string = 'find -name *.mp3'
        a = subprocess.Popen(shlex.split(string), stdout=subprocess.PIPE)
        res, err = a.communicate()
        return [os.path.abspath(line) for line in res.decode('utf-8').splitlines()]

    def toDict(self, location):
        mp3tags = mp3(location)
        return (mp3tags['artist'][0], mp3tags['title'][0])

if __name__ == '__main__':
    InitDB()
