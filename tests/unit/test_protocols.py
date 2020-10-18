from unittest.mock import Mock

from pytest import raises

from pubsub.helpers import Message
from pubsub.protocols import BaseProtocol, EchoProtocol
from pubsub.serializers import BaseSerializer, JsonSerializer
from pubsub.transporters import BaseTransport
from tests._common import TEST_OBJ, TEST_TOPIC, EVENT_PAYLOAD, PERSON_PAYLOAD


def test_base_protocol():
    processor = BaseProtocol(
        transport=BaseTransport(), serializer=BaseSerializer()
    )
    assert isinstance(processor, BaseProtocol)
    assert isinstance(processor.serializer, BaseSerializer)
    assert isinstance(processor.transport, BaseTransport)

    processor.transport.publish = Mock()
    processor.publish(TEST_TOPIC, TEST_OBJ)
    processor.transport.publish.assert_called_with(TEST_TOPIC, None)

    processor.transport.subscribe = Mock()
    processor.subscribe(TEST_TOPIC)
    processor.transport.subscribe.assert_called_with(
        TEST_TOPIC, callback=processor.handle_payload
    )


def test_regex_pre_filter():
    pre_filter = r"\"schema\": \"(.*)events/cart/created/1.0.json\""
    processor = BaseProtocol(
        transport=BaseTransport(),
        serializer=BaseSerializer(),
        pre_filter=pre_filter,
    )
    assert processor.regex_filter(EVENT_PAYLOAD) is not None
    assert processor.regex_filter(PERSON_PAYLOAD) is None


def test_base_handle_payload():
    pre_filter = r"\"schema\": \"(.*)events/product/created/1.0.json\""
    processor = BaseProtocol(
        transport=BaseTransport(),
        serializer=JsonSerializer(),
        pre_filter=pre_filter,
    )
    processor.handle_message = Mock()
    processor.handle_payload(EVENT_PAYLOAD)
    processor.handle_message.assert_not_called()

    processor = BaseProtocol(
        transport=BaseTransport(),
        serializer=JsonSerializer(),
        wrap_in_message=True,
    )
    processor.handle_message = Mock()
    processor.handle_payload(EVENT_PAYLOAD)
    assert isinstance(processor.handle_message.call_args[0][0], Message)

    processor = BaseProtocol(
        transport=BaseTransport(),
        serializer=JsonSerializer(),
        wrap_in_message=False,
    )
    processor.handle_message = Mock()
    processor.handle_payload(EVENT_PAYLOAD)
    assert isinstance(processor.handle_message.call_args[0][0], dict)


def test_base_handle_message():
    processor = BaseProtocol(
        transport=BaseTransport(), serializer=BaseSerializer()
    )
    with raises(NotImplementedError):
        processor.handle_message({})


def test_base_handle_exception():
    processor = BaseProtocol(
        transport=BaseTransport(),
        serializer=BaseSerializer(),
        raise_exceptions=False,
    )
    processor.handle_exception(Exception())

    processor = BaseProtocol(
        transport=BaseTransport(),
        serializer=BaseSerializer(),
        raise_exceptions=True,
    )
    with raises(Exception):
        processor.handle_exception(Exception())


def test_echo_protocol(capsys):
    e = EchoProtocol(transport=BaseTransport(), serializer=BaseSerializer())
    e.handle_message(TEST_OBJ)
    captured = capsys.readouterr()
    assert captured.out.strip() == repr(TEST_OBJ).strip()
