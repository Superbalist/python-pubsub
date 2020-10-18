#!/usr/bin/env python

import functools
import sys
import timeit
from pathlib import Path

from humanize import naturalsize, intword
from tabulate import tabulate

from pubsub.helpers import Message
from pubsub.serializers.serializers import (
    JsonSerializer,
    UJsonSerializer,
    RapidJsonSerializer,
    OrJsonSerializer,
)

EXAMPLES_DIR = Path("tests/example_payloads")
EVENT_PAYLOAD = (EXAMPLES_DIR / "event.json").read_text()
LARGE_PAYLOAD = (EXAMPLES_DIR / "large.json").read_text()
MASSIVE_PAYLOAD = (EXAMPLES_DIR / "massive.json").read_text()
NESTED_PAYLOAD = (EXAMPLES_DIR / "nested.json").read_text()

RESULT_FILE = Path("docs/message-benchmarks.md")


def _get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([_get_size(v, seen) for v in obj.values()])
        size += sum([_get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += _get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(
        obj, (str, bytes, bytearray)
    ):
        size += sum([_get_size(i, seen) for i in obj])
    return size


def _get_message(payload, serializer):
    m = Message(obj=serializer.deserialize(payload))
    return m


def bench_payload(description, payload, number, serializer):
    serializer_name = type(serializer).__name__
    print(f"Running {description} using {serializer_name}")
    duration = timeit.timeit(
        functools.partial(_get_message, payload, serializer), number=number
    )
    print(f"Done in {duration:.3f} secs")
    obj = serializer.deserialize(payload)
    message = Message(obj=obj)
    message_size = _get_size(message)
    object_size = _get_size(obj)
    message_overhead = message_size - object_size
    return {
        "serializer": serializer_name,
        "bench_description": description,
        "duration_seconds": f"{duration:.3f}",
        "repetitions": intword(number),
        "payload_byte_size": naturalsize(len(payload.encode("utf-8"))),
        "message_overhead": naturalsize(message_overhead),
        "message_size": naturalsize(message_size),
        "object_size": naturalsize(object_size),
        "total_overhead": naturalsize(message_overhead * number),
    }


benchmarks = [
    functools.partial(bench_payload, "Small payload", EVENT_PAYLOAD, 100000),
    functools.partial(bench_payload, "Large payload", LARGE_PAYLOAD, 1000),
    functools.partial(bench_payload, "Massive payload", MASSIVE_PAYLOAD, 10),
    functools.partial(bench_payload, "Nested", NESTED_PAYLOAD, 10),
]

serializers = [
    JsonSerializer(),
]

if "ujson" in sys.modules:
    serializers.append(UJsonSerializer())

if "rapidjson" in sys.modules:
    serializers.append(RapidJsonSerializer())

if "orjson" in sys.modules:
    serializers.append(OrJsonSerializer())


if __name__ == "__main__":
    bench_result = [b(s) for s in serializers for b in benchmarks]
    table = tabulate(bench_result, headers="keys", tablefmt="github")
    RESULT_FILE.write_text(f"# Message benchmarks\n\n{table}")
    print("fin")
