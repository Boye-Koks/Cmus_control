#! /usr/bin/python3

import parsedata as pd
import os, sys
import subprocess, shlex

class Main(object):

    def __init__(self, config, database):
        self.database = database
        self.config = config

    def main(self):
        finished = False
        while(not finished):
            result = None
            song = self.askSong()
            if song:
                queue = input("Queue \"" + song['song'] + "\" by \"" + song['artist'] + "\"? (Y/n) ")
                if not queue == 'n':
                    self.queueSong(song)
                    result = "Queued \"" + song['song'] + "\" by \"" + song['artist'] + "\"!"
            else:
                result = "No songs found!"
            self.clearScreen()
            if result:
                print(result)
            finished = self.askFinished()

    def clearScreen(self):
        subprocess.call('clear')

    def askSong(self):
        songname = input("Type a query for matching songs, leave empty for all songs: ").strip()
        songs = self.database.findMatches(songname)
        selected_song = None
        if len(songs) == 0: # no songs found
            return None
        elif len(songs) > 1:
            result = ""
            i = 1
            nr_of_songs = len(songs)
            for d in songs:
                # .zfill(len(str(nr_of_songs)))
                songstring = "{0:8} {1:40} {2}\n".format(str(i), d['artist'], d['song'])
                result += songstring
                i += 1
            result += "Select one (or select 0 to not queue): "
            int_input = -1
            while int_input < 0:
                try:
                    int_input = int(input(result))
                except ValueError:
                    print("Not a valid number! Try again")
                if int_input > nr_of_songs:
                    self.clearScreen()
                    print("Not a valid number! Try again")
                    int_input = -1

            if not int_input == 0:
                selected_song = songs[int_input - 1]
        else:
            selected_song = songs[0]
        return selected_song

    def queueSong(self, song):
        command = shlex.split("ssh {0} 'cmus-remote -q {1}'".format(self.config['ssh_hostname'], song['location']))
        a = subprocess.Popen(command)

    def askFinished(self):
        result = input("Request another song? (Y/n) ")
        return result is 'n'

if __name__ == '__main__':
    try:
        Main(sys.argv[1::])
    except KeyboardInterrupt:
        print("\nExiting!")
