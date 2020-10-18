from pytest import raises

from pubsub.serializers import (
    BaseSerializer,
    SerializerException,
    JsonSerializer,
    UJsonSerializer,
    RapidJsonSerializer,
    OrJsonSerializer,
    MessagePackSerializer,
)

from tests._common import BROKEN_PAYLOAD


def test_base_serializer():
    s = BaseSerializer()
    s.deserialize("")
    s.serialize({})


def test_json_serializer():
    s = JsonSerializer()

    p = s.deserialize("{}")
    assert isinstance(p, dict)
    d = s.serialize({})
    assert isinstance(d, bytes)

    with raises(SerializerException):
        s.deserialize(BROKEN_PAYLOAD)

    with raises(SerializerException):
        s.serialize({"item": set()})


def test_ujson_serializer():
    s = UJsonSerializer()

    p = s.deserialize("{}")
    assert isinstance(p, dict)
    d = s.serialize({})
    assert isinstance(d, bytes)

    with raises(SerializerException):
        s.deserialize(BROKEN_PAYLOAD)


def test_rapidjson_serializer():
    s = RapidJsonSerializer()

    p = s.deserialize("{}")
    assert isinstance(p, dict)
    d = s.serialize({})
    assert isinstance(d, bytes)

    with raises(SerializerException):
        s.deserialize(BROKEN_PAYLOAD)

    with raises(SerializerException):
        s.serialize({"item": set()})


def test_orjson_serializer():
    s = OrJsonSerializer()

    p = s.deserialize("{}")
    assert isinstance(p, dict)
    d = s.serialize({})
    assert isinstance(d, bytes)

    with raises(SerializerException):
        s.deserialize(BROKEN_PAYLOAD)

    with raises(SerializerException):
        s.serialize({"item": set()})


def test_msgpack_serializer():
    s = MessagePackSerializer()

    p = s.deserialize(b"\x80")
    assert isinstance(p, dict)
    d = s.serialize({})
    assert isinstance(d, bytes)

    with raises(SerializerException):
        s.deserialize(BROKEN_PAYLOAD)

    with raises(TypeError):
        s.serialize({"item": set()})
