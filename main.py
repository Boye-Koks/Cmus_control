#! /usr/bin/python3

import sys, subprocess, os
import displayqueue as dq
import queuesongs as qs
import createdb as cdb
import parsedata as pd

def main(argv):
    socket = '127.0.0.1'
    passwd = '123456'
    path = None
    if len(argv) >= 1:
        path = argv[0]
    if len(argv) == 3:
        socket = argv[1]
        passwd = argv[2]

    database = pd.Database()
    queue_song = qs.Main([socket, passwd], database)
    show_queue = dq.Queue(socket, passwd)
    create_db = cdb.InitDB(database)
    print("Welcome!")
    while True:
        msg = None
        result = showMenu()
        clearScreen()
        if result == 1:
            queue_song.main()
        elif result == 2:
            show_queue.show()
        elif result == 3:
            if not path:
                path = getPath()
            print("Creating database...")
            create_db.create(path)
            msg = "Database created!"
        elif result == 4:
            print("Exiting!")
            quit()
        clearScreen()
        if msg:
            print(msg)

def showMenu():
    menu = "Select an option:\n1. Queue songs\n2. Show Queue\n3. Create database\n4. Quit\nSelection: "
    result = -1
    while not result > 0:
        try:
            result = int(input(menu))
        except ValueError:
            print("Invalid input, try again!")
        if result > 4:
            clearScreen()
            print("Invalid input, try again!")
            result = -1
    return result

def clearScreen():
    subprocess.call('clear')

def getPath():
    while True:
        path = input("Input the absolute path to the music database: ")
        if os.path.exists(path):
            return path
        else:
            clearScreen()
            print("Not a valid path!")

if __name__ == '__main__':
    try:
        main(sys.argv[1::])
    except KeyboardInterrupt:
        print("\nExiting!")
