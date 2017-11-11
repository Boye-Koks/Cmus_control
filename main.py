#! /usr/bin/python3

import sys, os, subprocess, shlex
import displayqueue as dq
import queuesongs as qs
import parsedata as pd

def main():

    clearScreen()

    config = initConfig()
    database = pd.Database()
    queue_song = qs.Main(config, database)
    show_queue = dq.Queue(config)

    datafile = initData(config)
    database.readDatabase(datafile)

    print("Welcome!")
    while True:
        msg = None
        result = showMenu()
        clearScreen()
        if result == 1:
            queue_song.main()
        elif result == 2:
            msg = show_queue.show()
        elif result == 3:
            print("Exiting!")
            quit()
        clearScreen()
        if msg:
            print(msg)

def showMenu():
    menu = "Select an option:\n1. Queue songs\n2. Show Queue\n3. Quit\nSelection: "
    result = -1
    while not result > 0:
        try:
            result = int(input(menu))
        except ValueError:
            print("Invalid input, try again!")
        if result > 3:
            clearScreen()
            print("Invalid input, try again!")
            result = -1
    return result

def readConfig():
    f = open('config', 'r')
    conflines = f.read().splitlines()
    config = dict([tuple(c.split('=')) for c in conflines])
    f.close()
    return config

def getData(config):
    command = shlex.split('scp {0}:{1} data'.format(config['ssh_hostname'], config['datafile']))
    subprocess.Popen(command, stdout=subprocess.PIPE).wait()

def clearScreen():
    subprocess.call('clear')

def initConfig():
    config = dict()
    if os.path.isfile('config'):
        config = readConfig()
    else:
        print("No config file found, create a config file and restart!")
        quit()

    if not 'local' in config:
        print("Missing mandatory field local, set local in config and restart!")
        quit()
    elif config['local'].lower() == 'false' and not 'ssh_hostname' in config:
        print("Missing ssh_hostname for remote server, set in config and restart!")
        quit()

    return config

def initData(config):
    datafile = config['datafile'] if 'datafile' in config else 'data'
    if os.path.isfile(datafile):
        return datafile
    elif 'local' in config and config['local'].lower() == 'true':
        print("No local data file found! Trying to load remote file at '{0}'".format(config['ssh_hostname']))
        try:
            getData(config)
            clearScreen()
            return datafile
            print("Remote data file loaded!")
        except:
            print("No remote data file found!\nExiting!")
            quit()
    else:
        print("No data file found! Create a data file using createdb")
        quit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting!")
