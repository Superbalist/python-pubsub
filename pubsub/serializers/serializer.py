import json


class Serializer:
    """
    Byte serializer to encode and decode messages
    """

    @staticmethod
    def encode(message):
        return message.encode()

    @staticmethod
    def decode(message):
        return message.data.decode()


class JSONSerializer:
    """
    JSONSerializer to encode and decode the message
    """

    @staticmethod
    def encode(message):
        return json.dumps(message).encode()

    @staticmethod
    def decode(message):
        return json.loads(message.data)
