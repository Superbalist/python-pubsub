# pubsub.py

A python abstraction for various pubsub providers.

[![Author](http://img.shields.io/badge/author-@superbalist-blue.svg?style=flat-square)](https://twitter.com/superbalist)
[![PyPI](https://img.shields.io/pypi/v/pubsub.py.svg?style=flat-square)](https://pypi.python.org/pypi/pubsub.py)
[![Github All Releases](https://img.shields.io/github/downloads/superbalist/pubsub.py/total.svg?style=flat-square)](https://github.com/Superbalist/pubsub.py)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://github.com/Superbalist/pubsub.py)

## Adapters

We plan to create python adapters for the following Pubsub providers, however currently only the GooglePubsub one is working.
* GoogleCloudAdapter - Working
* KafkaAdapter - Planned
* RedisAdapter - Planned

## Installation

```bash
pip install pubsub.py
```

## Usage

* Import the Protocol and any sub-modules you may require
* Instantiate a Protocol object that that takes the following parameters
  * adapter(Required)
  * serializer
  * validator
  * filter
* Use the Protcol to subscribe or publish.

```
from pubsub.protocol import Protocol
from pubsub.adapters.googlecloud import GooglePubsub


protocol = Protocol(adapter=GooglePubsub("GOOGLE_PROJECT_IDENTIFIER", client_identifier="CLIENT_IDENTIFIER"))
```

### Subscribe to a topic

```
# Create a callback handler method
def callback(message, data):
    print(data)

future = protocol.subscribe(topic='topic_name', callback=callback)

try:
    future.result()
except Exception as e:
    print(e)
```

And set an optional `exception_handler`:

```
# If you want to capture exceptions, you can create an optional exception handler, like one that uses Sentry

from raven import Client
sentry_client = Client()
def exception_handler(message, exc):
    sentry_client.captureException()

# If you use `always_raise=True` exceptions will be handed to `exception_handler` and then cause messages to remain unack'd
# If you use `always_raise=False` exceptions will be handed to `exception_handler` and you can choose to re-raise or ignore and ack messages

future = protocol.subscribe(topic='topic_name', callback=callback, exception_handler=exception_handler, always_raise=False)
```

### Publish a message to topic

```
protocol.publish('topic_name', 'Message')
```

`protocol.publish` also supports a custom `validation_error_callback`:

```
from datetime import datetime
from socket import gethostname
from uuid import uuid4


def validation_error_callback(invalid_message, exception, protocol):
    message = {
        'meta': {
            'date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'hostname': gethostname(),
            'service': 'example-app',
        },
        'message': invalid_message,
        'errors': [err.message for err in exception.errors]
    }
    protocol.publish('invalid-messages', message)
protocol.publish(topic, example_message, validation_error_callback)
```

## Tests

The tests currently use a MockGooglePubsub adapter to test code functionality rather than GooglePubsub connection.
