from requests import Session


class HttpAdapter(object):
    """
    PubSub adapter base class
    """
    def __init__(self, base_url=None):
        self.session = Session()
        self.base_url = base_url or 'http://127.0.0.1:3000'

    def publish(self, channel, message):
        response = self.session.post(
            '{}/messages/{}'.format(self.base_url, channel),
            data=message, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def subscribe(self, channel, callback, create_topic=False):
        raise NotImplementedError('Not implemented')

    def ack(self, message):
        pass
