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
        self.database = dict()
        for d in data:
            value = self.toDict(d.split(" | "))
            key = hash(value['location'])
            self.database[key] = value

    def toDict(self, songdata):
        result = dict()
        for val in songdata:
            result['artist'] = songdata[0]
            result['song'] = songdata[1]
            result['location'] = songdata[2]
        return result

    def findMatches(self, matchstring=None):
        if not matchstring:
            return sorted([self.database[k] for k in self.database], key=lambda x: x['artist'])
        matchstring = matchstring.lower()
        result = [self.database[k] for k in self.database if matchstring in self.database[k]['artist'].lower() or matchstring in self.database[k]['song'].lower()]
        return sorted(result, key=lambda x: x['artist'])
