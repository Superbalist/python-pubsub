from pubsub.serializers.serializer import JSONSerializer
from pubsub.validators.validator import ValidationError


class Protocol(object):
    """
    Protocol used to instantiate publisher/subscriber adapters with optional parameters(serializer, validator, filter)
    """

    def __init__(self, adapter, serializer=None, validator=None, validation_error_handler=None, filter=None):
        self.adapter = adapter
        self.serializer = serializer or JSONSerializer()
        self.validator = validator
        self.validation_error_handler = validation_error_handler
        self.filter = filter

    def publish(self, topic, message):
        if self.validator:
            try:
                self.validator.validate_message(message)
            except ValidationError as exc:
                if topic == 'validation_error':
                    raise Exception('Validation error event is invalid: {}. Errors: {}'.format(message, ','.join(err.message for err in exc.errors)))
                if self.validation_error_handler:
                    self.validation_error_handler(event=message, exception=exc, protocol=self)
                raise
        serialized = self.serializer.encode(message=message)
        self.adapter.publish(topic, serialized)

    def subscribe(
            self, topic, callback, exception_handler=lambda x, y: None, always_raise=True):

        def deserializer_callback(message):
            try:
                deserialized = self.serializer.decode(message)
                callback(message, deserialized)
            except Exception as exc:
                exception_handler(message, exc)
                if always_raise:
                    raise exc
            self.adapter.ack(message)

        return self.adapter.subscribe(topic, callback=deserializer_callback)

    def get_topics(self):
        return self.adapter.get_topics()

    def delete_topic(self, topic):
        self.adapter.delete_topic(topic)
