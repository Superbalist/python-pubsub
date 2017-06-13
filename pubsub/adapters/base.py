class BaseAdapter(object):
    """
    PubSub adapter base class
    """

    def __init__(self):
        pass

    def publish(self, channel, message):
        raise NotImplementedError('Not implemented')

    def subscribe(self, channel):
        raise NotImplementedError('Not implemented')
