#! /usr/bin/python3

import subprocess, shlex
from mutagen.mp3 import EasyMP3 as mp3

class Queue(object):

    def __init__(self, config, database):
        self.config = config
        self.database = database

    def show(self):
        if self.config['local'].lower() == 'true':
            command = shlex.split('cmus-remote -C "save -q -"')
        else:
            command = shlex.split("ssh {0} 'cmus-remote -C \"save -q -\"'".format(self.config['ssh_hostname']))
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        res, err = p.communicate()
        songs = res.decode('utf-8').splitlines()
        songdata = [(d['artist'], d['song']) for d in self.database.database if d['location'] in songs]
        songstring = self.listToString(songdata)
        return songstring

    def listToString(self, songdata):
        result = ""
        counter = 1
        for song in songdata:
            artist = song[0]
            title = song[1]
            songstring = "{0:8} {1:40} {2}\n".format(str(counter), artist, title)
            result += songstring
            counter += 1
        return result[:-1:]
