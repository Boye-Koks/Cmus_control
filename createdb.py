#! /usr/bin/python3

import os, sys
import subprocess, shlex
from mutagen.mp3 import EasyMP3 as mp3

class InitDB(object):

    def __init__(self
        self.database = dict()
        self.locations = list()

    def createDB(self):
        string = 'find -name *.mp3'
        a = subprocess.Popen(shlex.split(string), stdout=subprocess.PIPE)
        res, err = a.communicate()
        self.locations = res.decode('utf-8').splitlines()
        self.writeData()

    def writeData(self):
        mp3s = [mp3(l) for l in self.locations]
        data = [(d['artist'][0], d['title'][0]) for d in mp3s]
        self.database = [self.toDict([data[i][0], data[i][1], self.locations[i]]) for i in range(0,len(self.locations))]
        self.toFile()

    def toDict(self, songdata):
        result = dict()
        for val in songdata:
            result['artist'] = songdata[0]
            result['song'] = songdata[1]
            result['location'] = songdata[2]
        return result

    def toFile(self):
        filename = 'data'
        result = ""
        for val in self.database:
            artist = val['artist']
            song = val['song']
            location = val['location']
            result += artist + " | " + song + " | " + location + "\n"
        f = open(filename, "w")
        f.write(result)
        f.close()

if __name__ == '__main__':
    i = InitDB()
    i.createDB()
