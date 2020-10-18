import os
import logging

import httpx
from google.api_core.exceptions import AlreadyExists


import redis
from google.cloud import pubsub_v1
from tenacity import (
    retry,
    stop_after_attempt,
    retry_if_exception_type,
    wait_exponential,
)


BASE_URL_HTTP_DEFAULT = "http://127.0.0.1:3000/messages/"


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


class HTTPTransport(BaseTransport):
    def __init__(self, base_url: str = BASE_URL_HTTP_DEFAULT, *args, **kwargs):
        super(HTTPTransport, self).__init__(*args, **kwargs)
        self.client = httpx.Client(
            base_url=base_url, headers={"Content-Type": "application/json"}
        )

    def bulk_publish(self, channel, messages):
        return self.client.post(channel, data=messages)


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


class GooglePubsubTransport(BaseTransport):
    project: str
    subscription_name: str
    publisher: pubsub_v1.PublisherClient
    subscriber: pubsub_v1.SubscriberClient

    def __init__(
        self,
        project: str = os.getenv("GOOGLE_CLOUD_PROJECT"),
        name: str = "subscriber",
        *args,
        **kwargs,
    ):
        super(GooglePubsubTransport, self).__init__(*args, **kwargs)
        self.project = project
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_name = self.subscriber.subscription_path(
            self.project, name
        )

    def publish(self, topic, message):
        topic_name = self.subscriber.topic_path(self.project, topic)
        try:
            self.publisher.create_topic(topic_name)
        except AlreadyExists:
            pass

        self.publisher.publish(topic_name, message.encode())

    def subscribe(
        self,
        topic,
        callback,
        timeout=None,
        create=False,
        delete=False,
        **kwargs,
    ):
        topic_name = self.subscriber.topic_path(self.project, topic)
        if create:
            try:
                self.subscriber.create_subscription(
                    name=self.subscription_name, topic=topic_name
                )
            except AlreadyExists:
                self.logger.debug(
                    f"Subscription `{self.subscription_name}` "
                    f"to `{topic_name}` already exist"
                )

        future = self.subscriber.subscribe(
            self.subscription_name, callback, **kwargs
        )
        try:
            future.result(timeout)
        except Exception as exc:
            self.logger.exception(exc)
            if future.running():
                future.cancel()
        finally:
            if delete:
                self.subscriber.delete_subscription(self.subscription_name)
