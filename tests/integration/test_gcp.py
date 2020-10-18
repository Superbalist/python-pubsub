import os
from typing import Union

import docker
import pytest

from pubsub.serializers import JsonSerializer
from pubsub.helpers import Message
from pubsub.protocols import BaseProtocol
from pubsub.transporters import GooglePubsubTransport
from tests._common import MULTIPLE_EVENT_PAYLOADS, TEST_TOPIC, GCP_PROJECT_ID


class TestProtocol(BaseProtocol):
    def handle_message(self, message: Union[Message, dict]):
        print(repr(message))


@pytest.fixture
def server():
    client = docker.from_env()
    if not client.ping():
        pytest.exit("Could not connect to docker.")

    container = client.containers.run(
        image="messagebird/gcloud-pubsub-emulator:latest",
        hostname="gcloud-pubsub-emulator",
        ports={"8681/tcp": 8681},
        detach=True,
    )
    container.reload()
    host, port = container.ports["8681/tcp"].pop().values()

    os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT_ID
    os.environ["PUBSUB_EMULATOR_HOST"] = f"{host}:{port}"

    try:
        yield "localhost", int(port)
    finally:
        container.stop()
        container.remove()


@pytest.fixture
def protocol(server):
    t = GooglePubsubTransport(
        project=GCP_PROJECT_ID, name=f"{GCP_PROJECT_ID}-test"
    )
    s = JsonSerializer()
    p = TestProtocol(
        transport=t, serializer=s, wrap_in_message=True, raise_exceptions=True
    )
    return p


def test_publish(protocol):
    for payload in MULTIPLE_EVENT_PAYLOADS:
        protocol.publish(TEST_TOPIC, payload)
