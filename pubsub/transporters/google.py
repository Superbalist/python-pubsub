import os

from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

from pubsub.transporters.base import BaseTransport


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
        topic_name = self.publisher.topic_path(self.project, topic)
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
        topic_name = self.publisher.topic_path(self.project, topic)
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
