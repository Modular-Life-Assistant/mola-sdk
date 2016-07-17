import time

from mola_sdk.app.internal.InternalBaseApp import InternalBaseApp
from mola_sdk.event.internal.AppEventHelper import AppEventHelper


class BaseApp(InternalBaseApp, AppEventHelper):
    """This class is a template of methods to be implemented by apps."""
    def cron_day(self):
        """This method has been called one time by day"""
        pass

    def cron_hour(self):
        """This method has been called one time by day."""
        pass

    def cron_min(self):
        """This method has been called one time by min."""
        pass

    def cron_month(self):
        """This method has been called one time by month."""
        pass

    def cron_week(self):
        """This method has been called one time by week."""
        pass

    def cron_year(self):
        """This method has been called one time by year."""
        pass

    def init(self):
        """This app has been initialized."""
        pass

    def load_config(self):
        """Load app config."""
        pass

    def run(self):
        """This app loop running."""
        while self.is_running:
            time.sleep(5)

    def started(self):
        """This app has been started."""
        pass

    def stopped(self):
        """This app has been stopped."""
        pass
