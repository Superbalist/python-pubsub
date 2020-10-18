import httpx

from pubsub.transporters.base import BaseTransport


BASE_URL_HTTP_DEFAULT = "http://127.0.0.1:3000/messages/"


class HTTPTransport(BaseTransport):
    def __init__(self, base_url: str = BASE_URL_HTTP_DEFAULT, *args, **kwargs):
        super(HTTPTransport, self).__init__(*args, **kwargs)
        self.client = httpx.Client(
            base_url=base_url, headers={"Content-Type": "application/json"}
        )

    def bulk_publish(self, channel, messages):
        return self.client.post(channel, data=messages)