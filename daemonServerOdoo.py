import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import shlex, subprocess
import os

path_watch = ''  #Put here the paht from your root directory of your modules
path_make = ''   #Put here the path of your makefile
option_make = '' #Put here de option in your makefile

class MyHandler(PatternMatchingEventHandler):
    patterns=["*.py", "*.xml"]

    def process(self, event):

        os.chdir(path_make)
        out = os.popen('pidof python')
        for line in out:
            arrPid = line.split(' ')
            for pid in arrPid:
                outOdoo = os.popen('ps -Flww -p {0} | grep odoo'.format(pid.strip()))
                for lineOdoo in outOdoo:
                    os.system('kill -9 {0}'.format(pid.strip()))
        out.close()

        comand = 'make {0} &'.format(option_make)
        os.system(comand)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)



if __name__ == '__main__':
    observer = Observer()
    observer.schedule(MyHandler(), path_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
