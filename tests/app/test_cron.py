import threading
import time
import unittest

import sys

from mola_sdk.app.BaseApp import BaseApp


class CronCheck(BaseApp):
    day = None
    hour = None
    min = None
    month = None
    week = None
    year = None

    def cron_day(self):
        self.day = time.time()

    def cron_hour(self):
        self.hour = time.time()

    def cron_min(self):
        self.min = time.time()

    def cron_month(self):
        self.month = time.time()

    def cron_week(self):
        self.week = time.time()

    def cron_year(self):
        self.year = time.time()


class CronTestCase(unittest.TestCase):
    def setUp(self):
        self.time = time.time

    def tearDown(self):
        self.app.stop()
        sys.modules['time'].time = self.time

    def test_cron_call(self):
        self.app = CronCheck(parse_arg=False)
        assoc = {
            'day': 24*60*60,
            'hour': 60*60,
            'min': 60,
            'month': 30*24*60*60,
            'week': 7*24*60*60,
            'year': 365*24*60*60
        }

        for name, delta in assoc.items():
            # init values
            timestamp = 123456
            cron_type = 'cron_%s' % name
            sys.modules['time'].time = lambda: timestamp
            sys.modules['time'].time = lambda: timestamp
            self.app.save_file(cron_type, timestamp - delta)

            # run test
            threading.Thread(None, self.app.start).start()
            time.sleep(2)
            value = getattr(self.app, name)
            self.assertIsNotNone(value, name)
            self.assertEqual(value, timestamp, name)
            self.assertEqual(self.app.load_file(cron_type), timestamp, name)

            # clean
            self.app.stop()


if __name__ == '__main__':
    unittest.main()
