import logging
from re import search, compile
from typing import Optional, Union

from typing.re import Pattern

from pubsub.helpers import Message
from pubsub.serializers import BaseSerializer
from pubsub.transporters import BaseTransport


class BaseProtocol(object):
    transport: BaseTransport
    serializer: BaseSerializer
    filter_pattern: Optional[Pattern] = None
    wrap_in_message: bool
    raise_exceptions: bool
    logger: logging.Logger

    def __init__(
        self,
        transport: BaseTransport,
        serializer: BaseSerializer,
        pre_filter: str = "",
        wrap_in_message: bool = False,
        raise_exceptions: bool = False,
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self.logger = logger
        self.logger.info("Protocol initialise")
        self.transport = transport
        self.serializer = serializer
        self.wrap_in_message = wrap_in_message
        self.raise_exceptions = raise_exceptions
        if pre_filter:
            self.filter_pattern = compile(pre_filter)
        self.logger.info(self)

    def handle_payload(self, payload: Union[bytes, str]):
        try:
            if not self.regex_filter(payload):
                return

            message = self.serializer.deserialize(payload)

            if self.wrap_in_message:
                message = Message(obj=message)

            self.handle_message(message)
        except Exception as exc:
            self.handle_exception(exc, payload)

    def handle_message(self, message: Union[Message, dict]):
        pass

    def handle_exception(self, exc: Exception, payload: Union[bytes, str]):
        self.logger.exception(exc, payload)
        if self.raise_exceptions:
            raise exc

    def regex_filter(self, payload: str):
        if self.filter_pattern:
            return search(self.filter_pattern, payload)

        return True

    def publish(self, channel: str, message_obj: dict):
        self.transport.publish(channel, self.serializer.serialize(message_obj))

    def subscribe(self, channel: str, *args, **kwargs):
        self.transport.subscribe(channel, callback=self.handle_payload, *args, **kwargs)


class EchoProtocol(BaseProtocol):
    def handle_message(self, message: Union[Message, dict]):
        print(repr(message))
