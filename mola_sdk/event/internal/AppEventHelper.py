import logging
from collections import Callable

from mola_sdk.event import register_handler
from mola_sdk.event.message import *


class AppEventHelper(object):
    def __init__(self, *args, **kwargs):
        # search and binh event handler
        attributes = [getattr(self, f) for f in dir(self)]
        for handler in [f for f in attributes if callable(f)]:
            events_class = getattr(handler, 'events_class', None)
            if events_class is not None:
                register_handler(handler, *events_class)

    def alert_notify(self, text, image=None, sound=None):
        """Alert notify to human."""
        logging.error('Notify: %s %s %s' % (text, image, sound))
        Alert(self, image=image, sound=sound, text=text).fire()

    def notify(self, text, image=None, sound=None):
        """Notify to human."""
        logging.info('Notify: %s %s %s' % (text, image, sound))
        Notification(self, image=image, sound=sound, text=text).fire()

    def warning_notify(self, text, image=None, sound=None):
        """Warning notify to human."""
        logging.warning('Notify: %s %s %s' % (text, image, sound))
        Warning(self, image=image, sound=sound, text=text).fire()
