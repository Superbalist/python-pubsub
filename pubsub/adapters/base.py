class BaseAdapter(object):
    """
    PubSub adapter base class
    """

    def publish(self, channel, message):
        raise NotImplementedError('Not implemented')

    def subscribe(self, channel, callback):
        raise NotImplementedError('Not implemented')

    def ack(self, message):
        pass
