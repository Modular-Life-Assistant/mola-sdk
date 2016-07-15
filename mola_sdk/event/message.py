from mola_sdk.event.internal.Event import Event


class Notification(Event):
    """Message to human"""
    image = None
    sound = None
    text = ''


class Alert(Notification):
    """Alert to human"""
    pass


class Warning(Notification):
    """Warning to human"""
    pass
