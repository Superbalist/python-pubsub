from pubsub.serializers.serializer import JSONSerializer


class Protocol:
    """
    Protocol used to instantiate publisher/subscriber adapters with optional parameters(serializer, validator, filter)
    """

    def __init__(self, adapter, serializer=None, validator=None, filter=None):
        self.adapter = adapter
        self.serializer = serializer or JSONSerializer()
        self.validator = validator
        self.filter = filter

    def publish(self, topic, message):
        self.validator.validate_message(message)
        serialized = self.serializer.encode(message=message)
        self.adapter.publish(topic, serialized)

    def subscribe(self, topic):
        for message in self.adapter.subscribe(topic):
            serialized = self.serializer.decode(message)
            yield serialized
