import unittest
import os
from mock import Mock
from latte.Config import Config

class TestAnalyzer(unittest.TestCase):

    #def setUp(self):
        #self.config = Config()

    def testDefaultConfigs(self):
        """

        Tests if it uses default configs when user configs cannot be loaded.

        """
        self.config = Config('/tmp/non-existing-path')
        for (key, value) in self.config.get_default_configs().items():
            self.assertEquals(value, self.config.get(key))
