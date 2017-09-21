from google.cloud import pubsub
from google.gax.errors import GaxError
from grpc import StatusCode

from pubsub.adapters.base import BaseAdapter
from pubsub.adapters.exceptions import IdentifierRequiredException, TopicNotFound, SubscriptionNotFound


class GooglePubsub(BaseAdapter):
    """
    Google-cloud adapter class
    """

    def __init__(self, project_id, client_identifier='default'):
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        self.client_identifier = client_identifier
        self.project_id = project_id

    def publish(self, topic_name, message):
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        exists = True
        try:
            self.publisher.get_topic(topic_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            exists = False
        if not exists:
            self.publisher.create_topic(topic_path)
        self.publisher.publish(topic_path, message)

    def subscribe(self, topic_name):
        topic_path = self.subscriber.topic_path(self.project_id, '{}.{}'.format(self.client_identifier, topic_name))

        exists = True
        try:
            self.subscriber.get_topic(topic_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            exists = False
        if not exists:
            raise TopicNotFound("Can't subscribe to unknown topic: {}".format(topic_name))

        subscription = self.get_subscription(topic_name)

        while True:
            for ack_id, message in subscription.pull():
                yield message
                subscription.acknowledge([ack_id])

    def get_subscription(self, topic_name):
        if not self.client_identifier:
            raise IdentifierRequiredException("Use obj.set_client_identifier('name')")

        subscription_path = self.subscriber.subscription_path(self.project_id, self.client_identifier)
        try:
            return self.subscriber.get_subscription(subscription_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise

        try:
            return self.subscriber.create_subscription(subscription_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            raise TopicNotFound("Can't subscribe to unknown topic: {}".format(topic_name))

    def delete_topic(self, topic_name):
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        try:
            self.publisher.delete_topic(topic_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            raise TopicNotFound("Can't delete unknown topic: {}".format(topic_path))

    def delete_subscription(self):
        subscription_path = self.subscriber.subscription_path(self.project_id, self.client_identifier)
        try:
            self.subscriber.delete(subscription_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            raise SubscriptionNotFound("Can't delete unknown subscription: {}".format(subscription_path))
