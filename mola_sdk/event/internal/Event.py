import logging

from mola_sdk.event import get_handlers


class Event(object):
    def __init__(self, source, **kwargs):
        # get source infos
        self.source = source.__class__.__name__ if isinstance(source, object) \
            else str(source)

        # set attribute values
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def __str__(self):
        # get event values
        values = []
        for name, value in self.__dict__.items():
            if 'source' != name and value:
                values.append('%s="%s"' % (name, value))

        return '<Event: %s[%s] (%s)>' % (self.__class__.__name__,
                                         self.source, ', '.join(values))

    def fire(self):
        """Send event to network"""
        handlers = get_handlers(self.__class__)
        logging.debug('Fire event: %s(%d)' % (self, len(handlers)))
        for handler in handlers:
            handler(self)
