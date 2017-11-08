import logging
import threading
import time
from datetime import timedelta
from datetime import datetime

from pubsub.serializers.serializer import JSONSerializer

HEALTHCHECK_PERIOD = 60
HEALTHCHECK_TIMEOUT = 300

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

    def subscribe(self, topic, callback, exception_handler=lambda x, y: None, always_raise=True, healthcheck_period=HEALTHCHECK_PERIOD, healthcheck_timeout=HEALTHCHECK_TIMEOUT
                  ):
        lock = threading.Lock()
        global last_message
        last_message = datetime.utcnow()

        def deserializer_callback(message):
            with lock:
                global last_message
                last_message = datetime.utcnow()

            try:
                deserialized = self.serializer.decode(message)
                callback(message, deserialized)
            except Exception as exc:
                exception_handler(message, exc)
                if always_raise:
                    raise exc
            self.adapter.ack(message)

        self.adapter.subscribe(topic, callback=deserializer_callback)

        # The subscriber is non-blocking, so we must keep the main thread from
        # exiting to allow it to process messages in the background.
        while True:
            time.sleep(healthcheck_period)
            time_since_last = (datetime.utcnow() - last_message).total_seconds()
            if time_since_last > healthcheck_timeout:
                logging.critical("It's been a while since we saw a message. Subscribing thread might be dead.")
                break
