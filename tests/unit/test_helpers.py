from pubsub.serializers import SerializerException, JsonSerializer
from pytest import raises

from pubsub.helpers import Message, Dot
from tests._common import (
    TEST_OBJ,
    PERSON_PAYLOAD,
    BROKEN_PAYLOAD,
    EVENT_PAYLOAD,
)


def test_dot():
    d = Dot(**TEST_OBJ)
    assert isinstance(d, Dot)
    assert isinstance(d.tags, list)
    assert isinstance(d.relatives, list)
    assert isinstance(d.relatives[2], dict)
    assert d.relatives[4]["relation"] == "favorite mother"
    with raises(AttributeError):
        assert d.hobbies[0] == "hiking"

    assert isinstance(repr(d), str)


def test_message_creation():
    s = JsonSerializer()
    m = Message(s.deserialize(PERSON_PAYLOAD))

    assert isinstance(m, Message)
    assert isinstance(m.obj, Dot)


def test_message_serialization_fail():
    s = JsonSerializer()

    with raises(SerializerException):
        Message(s.deserialize(BROKEN_PAYLOAD))


def test_message_store():
    s = JsonSerializer()
    m = Message(s.deserialize(EVENT_PAYLOAD))

    # explicit Store object access
    assert m.obj.schema == "http://example.com/events/cart/created/1.0.json"
    assert m.obj.meta.uuid == "55e3d799-1ea5-48ab-b8ab-a1fb8460d448"

    # proxy access / intended usage
    assert m.meta.date == "2017-02-01T12:39:12+00:00"
    assert m.cart.is_expired is False
    assert isinstance(m.cart.items, list)
    assert isinstance(m.cart.items[0], Dot)
    assert m.cart.items[1].sku == "3S64LTC0IE"

    with raises(AttributeError):
        assert m.description is not None

    assert isinstance(repr(m), str)
    assert repr(m).startswith("Message ")
