import logging

from mola_sdk.event.message import *


class AppEventHelper(object):
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