import json
from typing import Union

try:
    import orjson
    import rapidjson
    import ujson
    import msgpack
except ImportError:  # pragma: no cover
    pass


class SerializerException(Exception):
    pass


class BaseSerializer:
    def deserialize(self, payload: Union[str, bytes]) -> object:
        pass

    def serialize(self, obj: object) -> bytes:
        pass


class JsonSerializer(BaseSerializer):
    def deserialize(self, payload: Union[str, bytes]) -> object:
        try:
            return json.loads(payload)
        except (json.JSONDecodeError, TypeError) as e:
            raise SerializerException(e)

    def serialize(self, obj: object) -> bytes:
        try:
            return json.dumps(obj, ensure_ascii=True).encode("utf-8")
        except Exception as e:
            raise SerializerException(e)


class OrJsonSerializer(BaseSerializer):
    def deserialize(self, payload: Union[str, bytes]) -> object:
        try:
            return orjson.loads(payload)
        except (json.JSONDecodeError, TypeError) as e:
            raise SerializerException(e)

    def serialize(self, obj: object) -> bytes:
        try:
            return orjson.dumps(obj)  # orjson dumps bytes, no need to encode
        except orjson.JSONEncodeError as e:
            raise SerializerException(e)


class RapidJsonSerializer(BaseSerializer):
    def deserialize(self, payload: Union[str, bytes]) -> object:
        try:
            return rapidjson.loads(payload)
        except (rapidjson.JSONDecodeError, TypeError) as e:
            raise SerializerException(e)

    def serialize(self, obj: object) -> bytes:
        try:
            return rapidjson.dumps(obj, ensure_ascii=True).encode("utf-8")
        except TypeError as e:
            raise SerializerException(e)


class UJsonSerializer(BaseSerializer):
    def deserialize(self, payload: Union[str, bytes]) -> object:
        try:
            return ujson.loads(payload)
        except Exception as e:
            raise SerializerException(e)

    def serialize(self, obj: object) -> bytes:
        # UJson is very forgiving, it will serialize whatever you give it.
        return ujson.dumps(obj, ensure_ascii=True).encode("utf-8")


class MessagePackSerializer(BaseSerializer):
    def deserialize(self, payload: Union[str, bytes]) -> object:
        try:
            if isinstance(payload, str):
                payload = payload.encode()

            return msgpack.unpackb(payload)
        except Exception as e:
            raise SerializerException(e)

    def serialize(self, obj: object) -> bytes:
        return msgpack.packb(obj)
