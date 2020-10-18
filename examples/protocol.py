from typing import Union

from icecream import ic

from pubsub import BaseProtocol, Message, GooglePubsubTransport, JsonSerializer
from pubsub.protocols import GooglePubsubProtocol

PROJECT_ID = "my-sandbox"
CHANNEL_NAME = "test"
SUBSCRIBER_NAME = "pubsub-test"


class MyProtocol(GooglePubsubProtocol):
    def handle_message(self, message: Message):
        ic(message)


if __name__ == '__main__':
    t = GooglePubsubTransport(project=PROJECT_ID, name=SUBSCRIBER_NAME)
    s = JsonSerializer()
    p = MyProtocol(
        transport=t,
        serializer=s,
        wrap_in_message=True,
        raise_exceptions=False
    )
    p.subscribe(CHANNEL_NAME, create=True, delete=False)
