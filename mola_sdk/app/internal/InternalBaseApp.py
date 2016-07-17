import argparse
import hmac
import json
import logging
import os
import threading
import gettext
import time

from _sha256 import sha256
from datetime import datetime


class InternalBaseApp(object):
    """This class implement the internal methods needed by modules."""
    files_path = '/tmp'
    is_running = False

    def __init__(self, parse_arg=True, **kwargs):
        self.init_log()
        if parse_arg:
            kwargs.update(self.__load_arg_command())

        # set data files path
        if kwargs.get('path'):
            self.files_path = kwargs['path']

        # set verbose level
        if kwargs.get('verbose'):
            logging.getLogger().setLevel({
                1: logging.INFO,
            }.get(kwargs['verbose'], logging.DEBUG))

        super(InternalBaseApp, self).__init__(**kwargs)
        logging.info('init...')
        self.__init_internationalization()
        self.init()

    def delete_file(self, name):
        """Delete content data."""
        path = self.get_file_path(name)
        if os.path.isfile(path):
            os.remove(path)

    def get_file_path(self, name):
        """Get data file path."""
        filme_name = hmac.new(name.encode(), digestmod=sha256).hexdigest()
        return os.path.join(self.files_path, filme_name)

    def init_log(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')

    def load_file(self, name, default_value=None):
        """Get file content data."""
        path = self.get_file_path(name)

        if not os.path.isfile(path):
            return default_value

        with open(path, 'r') as f:
            return json.load(f)

    def save_file(self, name, content):
        """Save file content data."""
        with open(self.get_file_path(name), 'w') as f:
            json.dump(content, f)

    def start(self):
        """Start this app."""
        logging.info('run...')
        self.is_running = True
        self.started()
        threading.Thread(None, self.__internal_run, 'internal_run').start()
        self.run()

        logging.info('stop...')
        self.stop()
        self.stopped()

    def stop(self):
        """Stop this app."""
        self.is_running = False

    def __internal_run(self):
        # load last values
        last_timestamp_cron = {
            i: self.load_file('cron_%s' % i, 0)
            for i in ['day', 'hour', 'min', 'month', 'week', 'year']
        }

        # to datetime
        for name in ['month', 'year']:
            last_timestamp_cron[name] = datetime.fromtimestamp(
                last_timestamp_cron[name]
            )

        def diff_month(d1, d2):
            return (d1.year - d2.year) * 12 + d1.month - d2.month

        while self.is_running:
            current_time = time.time()
            current_datetime = datetime.fromtimestamp(current_time)

            # cron min
            if 60 <= current_time - last_timestamp_cron['min']:
                last_timestamp_cron['min'] = current_time
                self.__run_cron('min', current_time)

            # cron hour
            if 60 * 60 <= current_time - last_timestamp_cron['hour']:
                last_timestamp_cron['hour'] = current_time
                self.__run_cron('hour', current_time)

            # cron day
            if 24 * 60 * 60 <= current_time - last_timestamp_cron['day']:
                last_timestamp_cron['day'] = current_time
                self.__run_cron('day', current_time)

            # cron week
            if 7 * 24 * 60 * 60 <= current_time - last_timestamp_cron['week']:
                last_timestamp_cron['week'] = current_time
                self.__run_cron('week', current_time)

            # cron month
            if diff_month(current_datetime, last_timestamp_cron['month']):
                last_timestamp_cron['month'] = current_datetime
                self.__run_cron('month', current_time)

            # cron year
            if current_datetime.year > last_timestamp_cron['year'].year:
                last_timestamp_cron['year'] = current_datetime
                self.__run_cron('year', current_time)

            time.sleep(1)

    def __load_arg_command(self):
        parser = argparse.ArgumentParser(description='MoLA App')
        parser.add_argument('--path', action='store', default=self.files_path)
        parser.add_argument('-v', '--verbose', action='count', default=0)
        return vars(parser.parse_args())

    def __run_cron(self, cron_type, current_time):
        cron_type = 'cron_%s' % cron_type
        self.save_file(cron_type, current_time)
        threading.Thread(None, getattr(self, cron_type), cron_type).start()

    def __init_internationalization(self):
        # load translate file
        domain = self.__class__.__name__
        t = gettext.translation(domain, fallback=True,)
        t.install()

        # debug infos
        info = t.info()
        if info:
            logging.debug('load %s.mo translate' % domain)
            logging.debug('    current language: %s' % info['language'])
            logging.debug('    last edit: %s' % info['po-revision-date'])

        # binding
        self._ = t.gettext
