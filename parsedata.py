#! /usr/bin/python3
import sys
import os
from mutagen.mp3 import EasyMP3 as mp3

class Database(object):

    def __init__(self):
        self.database = list()

    def readDatabase(self, fromfile):
        f = open(fromfile)
        data = f.read().splitlines()
        f.close()
        self.database = [self.toDict(d.split(" | ")) for d in data]
        # self.toFile(fromfile)

    def toDict(self, songdata):
        result = dict()
        for val in songdata:
            result['artist'] = songdata[0]
            result['song'] = songdata[1]
            result['location'] = songdata[2]
        return result

    def findMatches(self, matchstring):
        matchstring = matchstring.lower()
        return [val for val in self.database if matchstring in val['artist'].lower() or matchstring in val['song'].lower()]
