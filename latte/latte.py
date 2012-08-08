#!/usr/bin/env python

"""

Latte - Linux Automatic Time Tracker

Collects window titles you are working on, categorizes them and tracks time for
each window individually. Stores log data to the filesystem.

"""

import time
import subprocess
import os
import atexit

from .TimeTracker import TimeTracker
from .Assigner import Assigner
from .Config import Config

class Latte(object):

    """ Main application class. """

    def __init__(self):
        self.configs = Config()
        self.categorizer = Assigner('category', self.configs)
        self.projectizer = Assigner('project', self.configs)
        self.tracker = TimeTracker(configs=self.configs,
                                   categorizer=self.categorizer,
                                   projectizer=self.projectizer)

        atexit.register(self.cleanup)

    def cleanup(self):
        """ On exit force dump log information. """
        self.tracker.dump_logs()

    def run(self):
        """ Primary application loop. """
        last_autosave = 0
        try:
            while True:
                title = get_active_window_title()
                idle = False
                if self.configs.get('idle_time') and self.configs.get('idle_time') < get_idle_time():
                    idle = True
                if title and not idle:
                    self.tracker.log(title)
                    stats = self.tracker.get_window_stats(title)
                    print title, \
                        repr(stats['categories']), \
                        repr(stats['project']), \
                        stats['time']
                elif idle:
                    print 'Idling...'

                time.sleep(self.configs.get('sleep_time'))
                # Track time since last save and do autosaves
                last_autosave += self.configs.get('sleep_time')
                if last_autosave >= self.configs.get('autosave_time'):
                    last_autosave = 0
                    self.tracker.dump_logs()
        except KeyboardInterrupt:
            print 'Exiting...'

def get_active_window_title():
    """ Fetches active window title using xprop. """
    try:
        active = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                                stdout=subprocess.PIPE)
        active_id = active.communicate()[0].strip().split()[-1]
        window = subprocess.Popen(["xprop", "-id", active_id, "WM_NAME"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return window.communicate()[0].strip().split('"', 1)[-1][:-1]
    except:
        return ''

def get_idle_time():
    """ Fetches user idle time using xprintidle. """
    try:
        idle_time = subprocess.check_output(['xprintidle'])
        return int(idle_time) / 1000 # from miliseconds to seconds
    except OSError:
        return 0


if __name__ == '__main__':
    Latte().run()
