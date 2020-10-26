import logging


class BaseTransport:
    logger: logging.Logger

    def __init__(self, *args, **kwargs):
        if "logger" in kwargs.keys():
            self.logger = kwargs["logger"]
        else:
            self.logger = logging.getLogger(__name__)

    def publish(self, channel, message):
        pass

    def subscribe(self, channel, callback):
        pass

    @staticmethod
    def get_payload(message):
        return message
