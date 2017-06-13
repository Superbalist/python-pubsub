from google.cloud import pubsub
from pubsub.adapters.base import BaseAdapter
from pubsub.adapters.exceptions import IdentifierRequiredException, TopicNotFound, SubscriptionNotFound


class GooglePubsub(BaseAdapter):
    """
    Google-cloud adapter class
    """

    def __init__(self, client_identifier='default'):
        self.pubsub_client = pubsub.Client()
        self.client_identifier = client_identifier

    def publish(self, topic_name, message):
        topic = self.pubsub_client.topic(topic_name)
        if not topic.exists():
            topic.create()
        topic.publish(message)

    def subscribe(self, topic_name):
        topic = self.pubsub_client.topic(topic_name)
        subscription = self.make_subscription(topic)

        if not topic.exists():
            raise TopicNotFound("Can't subscribe to unknown topic: {}".format(topic_name))
        if not subscription.exists():
            subscription.create()

        while True:
            for ack_id, message in subscription.pull():
                yield message
                subscription.acknowledge([ack_id])

    def make_subscription(self, topic):
        if self.client_identifier:
            subscription_name = '{}.{}'.format(self.client_identifier, topic.name)
        else:
            raise IdentifierRequiredException("Use obj.set_client_identifier('name')")
        return topic.subscription(subscription_name)

    def delete_topic(self, topic):
        try:
            topic.delete()
        except Exception:
            raise TopicNotFound("Can't delete unknown topic: {}".format(topic.name))

    def delete_subscription(self, subscription):
        try:
            subscription.delete()
        except Exception:
            raise SubscriptionNotFound("Can't delete unknown subscription: {}".format(subscription.name))
