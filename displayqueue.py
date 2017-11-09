#! /usr/bin/python3

import subprocess, shlex
from mutagen.mp3 import EasyMP3 as mp3

class Queue(object):

    def __init__(self, socket, passwd):
        self.socket = socket
        self.passwd = passwd

    def show(self):
        command = shlex.split('cmus-remote --server {0} --passwd {1} -C "save -q -"'.format(self.socket, self.passwd))
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        res, err = p.communicate()
        songs = res.decode('utf-8').splitlines()
        mp3s = [mp3(s) for s in songs]
        songdata = [(s['artist'][0], s['title'][0]) for s in mp3s]
        songstring = self.listToString(songdata)
        print(songstring)

    def listToString(self, songdata):
        result = ""
        for song in songdata:
            artist = song[0]
            title = song[1]
            songstring = "{0:40}{1}\n".format(artist, title)
            result += songstring
        return result[:-1:]

if __name__ == '__main__':
    q = Queue('127.0.0.1', '123456')
    q.show()
