import logging
from unittest.mock import Mock, call, PropertyMock

import pytest
import respx
from google.api_core.exceptions import AlreadyExists

from pubsub.transporters import (
    BaseTransport,
    RedisTransport,
    HTTPTransport,
    GooglePubsubTransport,
)

from tests._common import (
    MULTIPLE_EVENT_PAYLOADS,
    EVENT_PAYLOAD,
    GCP_PROJECT_ID,
    TEST_TOPIC,
    TEST_PATTERN,
    HTTP_BASE_URL,
    TEST_OBJ,
    MULTIPLE_EVENT_PAYLOADS_GCP,
)


def _raise_already_created_exception(*args, **kwargs):
    raise AlreadyExists(f"Already exists")


def _raise_generic_exception(*args, **kwargs):
    raise Exception(f"An exception")


def test_base_protocol():
    t = BaseTransport()
    assert isinstance(t, BaseTransport)
    assert isinstance(t.logger, logging.Logger)

    t.publish(TEST_TOPIC, TEST_OBJ)
    m = Mock()
    t.subscribe(TEST_TOPIC, callback=m)

    logger_name = "MyLogger"
    logger = logging.getLogger(logger_name)
    t2 = BaseTransport(logger=logger)
    assert isinstance(t2, BaseTransport)
    assert isinstance(t2.logger, logging.Logger)
    assert t2.logger.name == logger_name


@respx.mock
def test_http_transport():
    h_t = HTTPTransport(base_url=HTTP_BASE_URL)
    request = respx.post(f"{HTTP_BASE_URL}{TEST_TOPIC}", status_code=200)
    response = h_t.bulk_publish(TEST_TOPIC, MULTIPLE_EVENT_PAYLOADS)
    assert request.called
    assert response.status_code == 200


def test_redis_transport_publish():
    t = RedisTransport()
    t.r.publish = Mock()
    for payload in MULTIPLE_EVENT_PAYLOADS:
        t.publish(TEST_TOPIC, payload)


def test_redis_transport_subscribe():
    t = RedisTransport()
    mock_callback = Mock()
    redis = Mock()
    redis.subscribe = Mock()
    redis.listen = Mock(return_value=iter(MULTIPLE_EVENT_PAYLOADS_GCP))
    t.r.pubsub = Mock(return_value=redis)

    t.subscribe(TEST_TOPIC, callback=mock_callback)
    calls = [call(p) for p in MULTIPLE_EVENT_PAYLOADS]
    mock_callback.assert_has_calls(calls)


def test_redis_transport_pattern_subscribe():
    t = RedisTransport()
    mock_callback = Mock()
    redis = Mock()
    redis.subscribe = Mock()
    redis.listen = Mock(return_value=iter(MULTIPLE_EVENT_PAYLOADS_GCP))
    t.r.pubsub = Mock(return_value=redis)

    t.pattern_subscribe(TEST_PATTERN, callback=mock_callback)
    calls = [call(p) for p in MULTIPLE_EVENT_PAYLOADS]
    mock_callback.assert_has_calls(calls)


def test_google_cloud_transport_publish():
    t = GooglePubsubTransport(project=GCP_PROJECT_ID)

    t.publisher.create_topic = Mock()
    t.publisher.publish = Mock()

    for payload in MULTIPLE_EVENT_PAYLOADS:
        t.publish(TEST_TOPIC, payload)

    t.publisher.create_topic.assert_called()
    topic_name = t.subscriber.topic_path(GCP_PROJECT_ID, TEST_TOPIC)
    calls = [call(topic_name, p.encode()) for p in MULTIPLE_EVENT_PAYLOADS]
    t.publisher.publish.assert_has_calls(calls)

    t.publisher.create_topic.reset()
    t.publisher.create_topic.side_effect = _raise_already_created_exception
    t.publish(TEST_TOPIC, EVENT_PAYLOAD)
    t.publisher.create_topic.assert_called()


def test_google_cloud_transport_subscribe():
    t = GooglePubsubTransport(project=GCP_PROJECT_ID)

    mock_callback = Mock()
    gcp = Mock()
    gcp.result = Mock(return_value=iter(MULTIPLE_EVENT_PAYLOADS))
    gcp.running = Mock(return_value=True)
    gcp.cancel = Mock()
    t.subscriber.subscribe = Mock(return_value=gcp)
    t.subscriber.create_subscription = Mock()
    t.subscriber.delete_subscription = Mock()

    t.subscribe(TEST_TOPIC, callback=mock_callback)
    t.subscriber.create_subscription.assert_not_called()

    t.subscriber.create_subscription.reset()
    t.subscribe(TEST_TOPIC, callback=mock_callback, create=True)
    t.subscriber.create_subscription.assert_called()

    t.subscriber.create_subscription.side_effect = (
        _raise_already_created_exception
    )
    t.subscribe(TEST_TOPIC, callback=mock_callback, create=True)
    t.subscriber.create_subscription.assert_called()

    t.subscriber.subscribe.reset()
    gcp.result.side_effect = _raise_generic_exception
    t.subscribe(TEST_TOPIC, callback=mock_callback, delete=True)
    gcp.cancel.assert_called()
    t.subscriber.delete_subscription.assert_called()
