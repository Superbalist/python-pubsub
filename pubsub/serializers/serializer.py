import json


class Serializer:
    """
    Byte serializer to encode and decode messages
    """

    @staticmethod
    def encode(message):
        return message.encode('utf-8')

    @staticmethod
    def decode(message):
        return message.data.decode('utf-8')


class JSONSerializer:
    """
    JSONSerializer to encode and decode the message
    """

    @staticmethod
    def encode(message):
        return json.dumps(message).encode('utf-8')

    @staticmethod
    def decode(message):
        return json.loads(message.data.decode('utf-8'))
