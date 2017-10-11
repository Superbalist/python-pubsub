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

    def subscribe(self, topic, callback=None):
        if callback is None:
            def callback(message):
                print('Received message: {}'.format(message))
                message.ack()

        def deserializer_callback(message):
            serialized = self.serializer.decode(message)
            callback(serialized)

        self.adapter.subscribe(topic, callback=deserializer_callback)
