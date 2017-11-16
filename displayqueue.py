#! /usr/bin/python3

import subprocess, shlex
from mutagen.mp3 import EasyMP3 as mp3

class Queue(object):

    def __init__(self, config, database):
        self.config = config
        self.database = database

    def show(self):
        # Get current song
        if self.config['local'].lower() == 'true':
            command = ['cmus-remote', '-Q']
        else:
            command = ['ssh', self.config['ssh_hostname'], 'cmus-remote -Q']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        res, err = p.communicate()
        songhash = hash(res.decode('utf-8').splitlines()[1].strip('file '))
        songdata = [self.database.database[songhash]]

        # Get queued songs
        if self.config['local'].lower() == 'true':
            command = shlex.split('cmus-remote -C "save -q -"')
        else:
            command = shlex.split("ssh {0} 'cmus-remote -C \"save -q -\"'".format(self.config['ssh_hostname']))
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        res, err = p.communicate()
        songs = res.decode('utf-8').splitlines()
        hashes = map(hash, songs)
        songdata += [self.database.database[x] for x in hashes]
        # songstring = self.listToString(songdata)
        if not songdata:
            return [-1]
        return songdata

    def listToString(self, songdata):
        result = ""
        counter = 1
        for song in songdata:
            artist = song['artist']
            title = song['song']
            songstring = "{0:8} {1:40} {2}\n".format(str(counter), artist, title)
            result += songstring
            counter += 1
        return result[:-1:]
