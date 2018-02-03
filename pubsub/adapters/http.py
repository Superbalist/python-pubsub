from requests import Session


class HttpAdapter(object):
    """
    PubSub adapter base class
    """
    def __init__(self, base_url=None):
        self.session = Session()
        self.base_url = base_url or 'http://127.0.0.1:3000'

    def bulk_publish(self, channel, messages):
        # We could use json=, but the message is already dumped and encoded
        response = self.session.post(
            '{}/messages/{}'.format(self.base_url, channel),
            data=messages, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()

    def ack(self, message):
        pass
