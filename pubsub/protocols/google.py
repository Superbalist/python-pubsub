from pubsub import GooglePubsubTransport, JsonSerializer
from pubsub.protocols.base import BaseProtocol


class GooglePubsubProtocol(BaseProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(
            transport=GooglePubsubTransport(),
            serializer=JsonSerializer(),
            *args, **kwargs
        )

    def handle_payload(self, message):


