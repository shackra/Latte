import ctypes
import os

import lattex11


class UserActivityTracker(object):
    def __init__(self, time_tracker, config):
        self.time_tracker = time_tracker
        self.config = config
        self.user_inactive = False
        self.inactive_tracking_available = 'DISPLAY' in os.environ

    def is_inactive_tracking_available(self):
        """ Checks whether inactivity tracking is available """
        return self.inactive_tracking_available

    def is_user_inactive(self):
        """ Checks whether the user is inactive based on inactivity threshold """
        inactivity_duration = self.get_inactivity_time()
        if inactivity_duration > self.config.get('user_inactive_threshold'):
            if not self.user_inactive:
                self.time_tracker.reduce_time(inactivity_duration)
                self.user_inactive = True
        else:
            self.user_inactive = False
        return self.user_inactive

    def get_inactivity_time(self):
        if self.is_inactive_tracking_available():
            return lattex11.get_inactivity_time()
