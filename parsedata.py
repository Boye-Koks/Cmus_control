#! /usr/bin/python3
import sys
import os.path
from mutagen.mp3 import EasyMP3 as mp3

class Database(object):

    def __init__(self):
        self.database = list()

    def writeData(self, fromfile, tofile):
        location_file = open(fromfile)
        locations = location_file.read().splitlines()
        location_file.close()
        mp3s = [mp3(l) for l in locations]
        data = [(d['artist'][0], d['title'][0]) for d in mp3s]
        self.database = [self.toDict([data[i][0], data[i][1], os.path.abspath(locations[i])]) for i in range(0,len(locations))]
        self.toFile(tofile)

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

    def toFile(self, filename):
        f = open(filename, "w")
        result = ""
        for val in self.database:
            artist = val['artist']
            song = val['song']
            location = val['location']
            result += artist + " | " + song + " | " + location + "\n"
        f.write(result)
        f.close()

    def findMatches(self, matchstring):
        matchstring = matchstring.lower()
        return [val for val in self.database if matchstring in val['artist'].lower() or matchstring in val['song'].lower()]
