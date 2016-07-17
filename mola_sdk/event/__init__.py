from functools import wraps

handlers_binding = {}


def event(*events_class):
    """ Event handler decorator.

    :param events_class: event(s) to binding
    """
    def wrap(f):
        f.events_class = events_class
        return f
    return wrap


def get_handlers(event_class):
    """Get all handler of event.

    :param event_class: event class
    :return: handlers list
    """
    return handlers_binding[event_class] if event_class in handlers_binding \
        else []


def register_handler(handler, *events_class):
    """Register a handler for event(s)

    :param handler: function to register
    :param events_class: event(s) to binding
    """
    for event_class in events_class:
        if event_class in handlers_binding:
            handlers_binding[event_class].append(handler)
        else:
            handlers_binding[event_class] = [handler]
