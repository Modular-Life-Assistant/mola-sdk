import time
import threading
import unittest

from mola_sdk.app.BaseApp import BaseApp
from mola_sdk.event import event
from mola_sdk.event.message import *



class EventCheck(BaseApp):
    notify_test = None

    @event(Notification)
    def notify_handler(self, event):
        self.notify_test = event


class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.app = EventCheck(parse_arg=False)
        threading.Thread(None, self.app.start).start()

    def tearDown(self):
        self.app.stop()

    def test_notification(self):
        self.app.notify('test')

        time.sleep(2)

        event = self.app.notify_test
        self.assertIsNotNone(event)
        self.assertIsInstance(event, Notification)
        self.assertEqual(event.text, 'test')
        self.assertIsNone(event.image)
        self.assertIsNone(event.sound)


if __name__ == '__main__':
    unittest.main()
