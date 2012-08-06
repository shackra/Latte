import unittest
import os
import mock
import time
from latte.Analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.configs = {}
        self.configs['appPath'] = os.path.expanduser('latte/')
        self.configs['statsPath'] = 'stats/'
        self.configs['sleepTime'] = 5
        self.configs['autosaveTime'] = 3600

        self.analyzer = Analyzer(self.configs)
        self.allowedTimeImprecisionInSeconds = 1

    def tearDown(self):
        pass

    def testNormalizeTime(self):
        """ Tests time normalization """
        self.assertEqual(self.analyzer.normalize_time(0), '0s')
        self.assertEqual(self.analyzer.normalize_time(-1), '0s')
        self.assertEqual(self.analyzer.normalize_time(10), '10s')
        self.assertEqual(self.analyzer.normalize_time(60), '1m0s')
        self.assertEqual(self.analyzer.normalize_time(119), '1m59s')
        self.assertEqual(self.analyzer.normalize_time(3600), '1h0m0s')
        self.assertEqual(self.analyzer.normalize_time(3661), '1h1m1s')

    def testCalculateSince(self):
        """ Tests Calculate since. """
        self.assertEqual(self.analyzer.calculate_since('0'), 0)
        self.assertEqual(self.analyzer.calculate_since('-1'), 0)
        self.assertAlmostEqual(self.analyzer.calculate_since('20'), time.time() - 20, delta=self.allowedTimeImprecisionInSeconds)
        # With multiplier
        oneDayAgo = time.time() - 60 * 60 * 24
        self.assertAlmostEqual(self.analyzer.calculate_since('1', 'd'), oneDayAgo, delta=self.allowedTimeImprecisionInSeconds)
        twoWeeksAgo = time.time() - 60 * 60 * 24 * 7 * 2
        self.assertAlmostEqual(self.analyzer.calculate_since('2', 'w'), twoWeeksAgo, delta=self.allowedTimeImprecisionInSeconds)
        threeMonthsAgo = time.time() - 60 * 60 * 24 * 30 * 3
        self.assertAlmostEqual(self.analyzer.calculate_since('3', 'm'), threeMonthsAgo, delta=self.allowedTimeImprecisionInSeconds)
        # Cannot convert to number
        self.assertFalse(self.analyzer.calculate_since('crash'))
