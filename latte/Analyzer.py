"""

Latte activity log analyzer

"""

import os
import json
import time

from .Config import Config

class Analyzer(object):
    """ Analyzes Latte log data """

    def __init__(self, config, args=[]):
        self.config = config
        self.logs = {}
        self.parse_time_args(args)

    def parse_time_args(self, args=[]):
        self.since = time.time() - 86400 # Default to 1 day
        if len(args) == 1:
            self.since = self.calculate_since(args[0])
        elif len(args) == 2 and args[1] in ['d', 'w', 'm']:
            self.since = self.calculate_since(args[0], args[1])

    def calculate_since(self, since_str, multiplier=''):
        try:
            log_time = int(since_str, 10)
            if log_time <= 0: # Don't allow peeking into the future
                return 0
            if multiplier:
                multipliers = {
                    'd' : 86400, # 1 day
                    'w' : 604800, # 1 week
                    'm' : 2592000 # 1 month
                }
                log_time *= multipliers[multiplier]
            return time.time() - log_time
        except ValueError:
            print 'Cannot convert time argument to integer'
            return False

    def run(self):
        """ Main analyzer loop """
        self.load_logs()
        self.analyze()
        self.print_log_data()

    def analyze(self):
        """ Analyzes log data """
        if self.since:
            print 'Looking for log data since %s' % time.strftime('%d %b %Y %H:%M:%S', time.gmtime(self.since))
        if not self.logs:
            print 'There is no log data'
            return False

        self.windows = {}
        self.categories = {}
        self.projects = {}
        self.totalLogs = 0
        self.totalTime = 0

        # Log files
        for logFileKey in self.logs.keys():
            logFile = self.logs[logFileKey]
            self.totalLogs += len(logFile)
            # Individual log entries
            for logKey in logFile.keys():
                log = logFile[logKey]
                self.totalTime += log['time']
                if not self.windows.has_key(logKey):
                    self.windows[logKey] = log['time']
                else:
                    self.windows[logKey] += log['time']
                if not self.projects.has_key(log['project']):
                    self.projects[log['project']] = log['time']
                else:
                    self.projects[log['project']] += log['time']
                if 'categories' in log.keys():
                    if not log['categories']:
                        log['categories'] = ['(Uncategorized)']
                    # Assign time to individual categories
                    for cat in log['categories']:
                        if not self.categories.has_key(cat):
                            self.categories[cat] = log['time']
                        else:
                            self.categories[cat] += log['time']


    def print_log_data(self):
        print 'Total log files: %d\nTotal log entries: %d' % (len(self.logs), \
                                                              self.totalLogs)
        print 'Total logged time: %s' % self.normalize_time(self.totalTime)
        print ''
        print 'Spent time on windows:'
        sortedWindowTimes = sorted(self.windows.items(), \
                                   cmp=lambda x, y: cmp(x[1], y[1]), \
                                   reverse=True)
        for (window, spent) in sortedWindowTimes:
            print '- "%s" : %s' % (window, self.normalize_time(spent))

        print ''
        print 'Spent time on categories:'
        for (category, spent) in self.categories.items():
            print '- "%s" : %s' % (category, self.normalize_time(spent))

        print ''
        print 'Spent time on projects:'
        for (project, spent) in self.projects.items():
            print '- "%s" : %s' % (project, self.normalize_time(spent))


    def load_logs(self):
        """ Loads logs from log files and stores them in memory """

        # Get a list of log files available
        logsPath = os.path.join(self.config.get('app_path'), \
                                self.config.get('stats_path'))
        logFiles = os.listdir(logsPath)
        if not logFiles:
            return False

        if self.since:
            since = str(self.since)
            logFiles = filter(lambda x: x >= since, logFiles)


        # Attempt to open each file, read and parse log data
        for logFile in logFiles:
            path = os.path.join(logsPath, logFile)
            logFileHandle = open(path, 'r')
            contents = logFileHandle.read()
            # File data may be corrupted
            try:
                jsonContents = json.loads(contents)
                self.logs[logFile] = jsonContents
            except ValueError:
                continue
            logFileHandle.close()
        return True

    def normalize_time(self, seconds):
        """ Normalizes time into user-friendly form """

        if seconds <= 0:
            return '0s'

        if seconds >= 60:
            minutes = seconds / 60
            seconds = seconds % 60
            if minutes >= 60:
                hours = minutes / 60
                minutes = minutes % 60
                return '%dh%dm%ds' % (hours, minutes, seconds)
            else:
                return '%dm%ds' % (minutes, seconds)
        else:
            return '%ds' % seconds

if __name__ == '__main__':
    Analyzer(Config()).run()
