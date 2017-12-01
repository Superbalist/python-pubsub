import logging

from google.cloud import pubsub_v1
from google.gax.errors import GaxError
from grpc import StatusCode

from pubsub.adapters.base import BaseAdapter
from pubsub.adapters.exceptions import IdentifierRequiredException, TopicNotFound, SubscriptionNotFound

log = logging.getLogger('pubsub')


class GooglePubsub(BaseAdapter):
    """
    Google-cloud adapter class
    """

    def __init__(self, project_id, client_identifier='default'):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.client_identifier = client_identifier
        self.project_id = project_id

    def ack(self, message):
        message.ack()

    def publish(self, topic_name, message):
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        try:
            self.publisher.get_topic(topic_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            self.publisher.create_topic(topic_path)
        self.publisher.publish(topic_path, message)

    def subscribe(self, topic_name, callback):
        # This makes sure the subscription exists
        self.get_subscription(topic_name)

        subscription_path = self.subscriber.subscription_path(self.project_id, '{}.{}'.format(self.client_identifier, topic_name))

        log.info('Starting to listen on: %s', subscription_path)
        policy = self.subscriber.subscribe(subscription_path)
        return policy.open(callback=callback)

    def get_subscription(self, topic_name):
        if not self.client_identifier:
            raise IdentifierRequiredException("Use obj.set_client_identifier('name')")

        subscription_path = self.subscriber.subscription_path(self.project_id, '{}.{}'.format(self.client_identifier, topic_name))
        try:
            return self.subscriber.get_subscription(subscription_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise

        topic_path = self.subscriber.topic_path(self.project_id, topic_name)
        try:
            return self.subscriber.create_subscription(subscription_path, topic_path)
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

    def delete_subscription(self, topic_name):
        subscription_path = self.subscriber.subscription_path(self.project_id, '{}.{}'.format(self.client_identifier, topic_name))
        try:
            self.subscriber.delete_subscription(subscription_path)
        except GaxError as exc:
            if exc.cause._state.code != StatusCode.NOT_FOUND:
                raise
            raise SubscriptionNotFound("Can't delete unknown subscription: {}".format(subscription_path))

    def get_topics(self):
        project_path = self.publisher.project_path(self.project_id)
        return self.publisher.list_topics(project_path)
