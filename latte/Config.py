"""

Config class

Handles application configuration loading

"""

import ConfigParser
import os

class Config(object):
    """ Handles config loading and parsing. """

    def __init__(self, path='~/.latte'):
        self.configs = {}
        self.user_config_path = os.path.expanduser(path)

        self.load_default_configs()
        self.create_default_configs()
        self.load_user_config(path)

    def get_default_configs(self):
        defaults = {
            'app_path' : self.user_config_path,
            'stats_path' : 'stats/',
            'sleep_time' : 5,
            'autosave_time' : 3600,
            'idle_time' : 900
        }
        return defaults

    def load_default_configs(self):
        """ Load default config values. """
        for (key, value) in self.get_default_configs().items():
            self.set(key, value)

    def set(self, name, value):
        """ Set config value. """
        self.configs[name] = value

    def create_default_configs(self):
        # Create main application folder
        if not os.path.exists(self.configs.get('app_path')):
            os.makedirs(self.configs.get('app_path'))

    def load_user_config(self, path):
        """ Attempt to load configs from default path. """
        path = os.path.expanduser(path + '/config')
        if os.path.exists(path):
            parser = ConfigParser.ConfigParser()
            parser.read(path)
            self.overwrite_with_user_configs(parser)
            return True
        else:
            return False

    def overwrite_with_user_configs(self, parser):
        """ Overwrite default configs with user-defined configs. """
        for item in ['stats_path']:
            self.set(item, parser.get('main', item))
        # Numeric values
        for item in ['sleep_time', 'autosave_time', 'idle_time']:
            self.set(item, parser.getint('main', item))

    def get(self, item):
        """ Fetches config item from the list. """
        if self.configs.has_key(item):
            return self.configs[item]
        return None

if __name__ == '__main__':
    Config()
