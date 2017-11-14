# -*- coding: utf-8 -*-
import threading
from collections import defaultdict, deque
from time import sleep
from unittest import TestCase

from google.cloud.pubsub_v1 import futures
from jsonschema import ValidationError

from pubsub.adapters.base import BaseAdapter
from pubsub.protocol import Protocol
from pubsub.serializers.serializer import JSONSerializer
from pubsub.validators.validator import SchemaValidator


class MockGoogleAdapter(BaseAdapter):
    """
    PubSub adapter base class
    """

    def __init__(self, client_identifier):
        self.client_id = client_identifier
        self._messages = defaultdict(deque)

    def publish(self, channel, message):
        self._messages[channel].appendleft(message)

    def subscribe(self, channel, callback):
        class MockMessage(object):
            def __init__(self, message):
                self.data = message

        future = futures.Future()

        def create_message():
            sleep(0.1)
            r = MockMessage(self._messages[channel].pop())
            try:
                return callback(r)
            except Exception as exc:
                future.set_exception(exc)

        thread = threading.Thread(target=create_message)
        thread.start()
        return future


class DoneException(Exception):
    pass


class ProtocolTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_message = {
            u'meta': {
                u'date': u'2017-02-01T12:39:12+00:00',
                u'hostname': u'superbalist-api-1935885982-59xk1',
                u'service': u'api',
                u'uuid': u'5AB2ABB6-8617-4DDA-81F7-DD47D5882B19'
            },
            u'schema': u'http://schema.superbalist.com/events/shopping_cart/created/1.0.json',
            u'shopping_cart': {
                u'id': 1070486,
                u'is_expired': False,
                u'is_restorable': True,
                u'items': [],
                u'user': {
                    u'email': u'matthew@superbalist.com',
                    u'first_name': u'Matthew',
                    u'id': 2,
                    u'last_name': u'G\u0151slett'
                }
            }
        }
        cls.invalid_message = {'blah': 'blah'}

    def test_valid_message(self):
        protocol = Protocol(
            adapter=MockGoogleAdapter('test-client'),
            serializer=JSONSerializer(),
            validator=SchemaValidator())
        protocol.publish('python_test', self.valid_message)

        def callback(message, data):
            assert data == self.valid_message
            raise DoneException()

        future = protocol.subscribe('python_test', callback=callback)
        with self.assertRaises(DoneException):
            future.result(timeout=1)

    def test_invalid_message(self):
        protocol = Protocol(
            adapter=MockGoogleAdapter('test-client'),
            serializer=JSONSerializer(),
            validator=SchemaValidator())
        with self.assertRaises(ValidationError):
            protocol.publish('python_test', self.invalid_message)

    # Only have one of these just to test its actually working
    # def test_real_google(self):
    #     protocol = Protocol(adapter=GooglePubsub(client_identifier='test_'), serializer=JSONSerializer(),
    #                         validator=SchemaValidator())
    #     protocol.publish('python_test', self.valid)
    #     sub = protocol.subscribe('python_test')
    #     for message in sub:
    #         assert message == self.valid
