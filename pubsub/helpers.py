import logging
from types import SimpleNamespace
from typing import Union

from pubsub.serializers import SerializerException


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Dot(SimpleNamespace):
    def __getattr__(self, item: str):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            raise

    def __repr__(self):
        return repr({k: self.__getattr__(k) for k in self.__dict__})


class Message:
    __slots__ = ("obj", )
    obj: Dot

    def __init__(self, obj: object):
        self.obj = self._unpack(obj)

    @staticmethod
    def _unpack(obj: object, depth: int = 3):
        if isinstance(obj, dict):
            if depth < 1:
                return Dot(**obj)

            for k, v in obj.items():
                obj[k] = Message._unpack(v, depth=depth - 1)

            obj = Dot(**obj)

        elif isinstance(obj, list):
            obj = [Message._unpack(v, depth=depth - 1) for v in obj]

        return obj

    def __getattr__(self, item: str):
        try:
            return getattr(self.obj, item)
        except Exception:
            raise AttributeError(f"No such attribute `{item}`")

    def __repr__(self):
        return f"Message {hex(id(self))}\n{self.obj}"

