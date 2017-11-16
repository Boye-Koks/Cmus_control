#! /usr/bin/python3

import subprocess, shlex

class Controller(object):

    def __init__(self, config):
        self.config = config

    def show(self):
        while(True):
            statement = "Select an option:\n1. Play/Pause\n2. Skip current song\n3. Restart current song\n4. Change volume\n5. Return\nSelection: "

            result = -1
            while not result > 0:
                try:
                    result = int(input(statement))
                except ValueError:
                    self.clearScreen()
                    print("Invalid input, try again!")
                if result > 6:
                    self.clearScreen()
                    print("Invalid input, try again!")
                    result = -1

            if result == 1:
                #play/pause
                msg = "Toggled play/pause!"
                self.playpause()
            elif result == 2:
                #skip
                msg = "Skipped!"
                self.skip()
            elif result == 3:
                #restart
                msg = "Restarted!"
                self.restart()
            elif result == 4:
                msg = self.changevolume()
            else:
                return True
            self.clearScreen()
            print(msg)

    def playpause(self):
        self.simplecommand('-u')

    def skip(self):
        self.simplecommand('-q -n')

    def restart(self):
        self.simplecommand('-q -r')

    def simplecommand(self, args):
        if self.config['local'].lower() == 'true':
            command = shlex.split('cmus-remote {0}').format(args)
        else:
            command = shlex.split("ssh {0} 'cmus-remote {1}'".format(self.config['ssh_hostname'], args))
        subprocess.call(command)

    def changevolume(self):
        return "Not yet implemented :("

    def clearScreen(self):
        subprocess.call('clear')
