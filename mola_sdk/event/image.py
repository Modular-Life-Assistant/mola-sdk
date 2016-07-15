from mola_sdk.event.internal.Event import Event


class ImageAnalysis(Event):
    """Image to analysis"""
    pass


class MotionImage(Event):
    """Image has motion"""
    pass


class StreamImage(Event):
    """Image of stream (1 per second)"""
    pass
