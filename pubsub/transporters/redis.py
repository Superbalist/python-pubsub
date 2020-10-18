import redis
from tenacity import (
    retry,
    stop_after_attempt,
    retry_if_exception_type,
    wait_exponential,
)

from pubsub.transporters.base import BaseTransport


class RedisTransport(BaseTransport):
    r: redis.Redis

    def __init__(self, host="localhost", port=6379, db=0, *args, **kwargs):
        super(RedisTransport, self).__init__(*args, **kwargs)
        self.r = redis.Redis(host, port, db, *args, **kwargs)

    def publish(self, channel, message):
        return self.r.publish(channel, message)

    @retry(
        retry=retry_if_exception_type(redis.exceptions.ConnectionError),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(2)
        # TODO: get tenacity working with instance logger?
        # before=before_log(self.logger, logging.DEBUG),
    )
    def subscribe(self, channel, callback):
        self.logger.debug(f"Subscribing to {channel}")
        p = self.r.pubsub(ignore_subscribe_messages=True)
        p.subscribe(channel)
        self.logger.debug("Listening...")
        for message in p.listen():
            self.logger.debug(f"Message received on `{message['channel']}`")
            callback(message["data"])

    @retry(
        retry=retry_if_exception_type(redis.exceptions.ConnectionError),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(2)
        # TODO: get tenacity working with instance logger?
        # before=before_log(self.logger, logging.DEBUG),
    )
    def pattern_subscribe(self, pattern, callback):
        self.logger.debug(f"Subscribing to {pattern}")
        p = self.r.pubsub(ignore_subscribe_messages=True)
        p.psubscribe(pattern)
        self.logger.debug("Listening...")
        for message in p.listen():
            self.logger.debug(
                f"Message received on `{message['channel']}` "
                f"using pattern `{message['pattern']}`"
            )
            callback(message["data"])
