# pubsub.py

A python abstraction for various puplisher subscribers.

[![Author](http://img.shields.io/badge/author-@superbalist-blue.svg?style=flat-square)](https://twitter.com/superbalist)
[![PyPI](https://img.shields.io/pypi/v/pubsub.py.svg?style=flat-square)](https://pypi.python.org/pypi/pubsub.py)
[![Github All Releases](https://img.shields.io/github/downloads/superbalist/pubsub.py/total.svg?style=flat-square)](https://github.com/Superbalist/pubsub.py)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://github.com/Superbalist/pubsub.py)

## Adapters

We plan to create python adapters for the following Pubsubs, however currently only the GooglePubsub one is working.
* GoogleCloudAdapter - Working
* KafkaAdapter - Planned
* RedisAdapter - Planned

## Installation

```bash
pip install pubsub.py
```

## Usage

* Import the Protocol and any sub-modules you may requre
* Instantiate a Protocol object that that takes the following parameters
  * adapter(Required)
  * serializer
  * validator
  * filter
* Use the Protcol to subscribe or publish.

```
from pubsub.protocol import Protocol
from pubsub.adapters.googlecloud import GooglePubsub


protocol = Protocol(adapter=GooglePubsub(client_identifier=sub_id))

# Subscribe to a topic
for message in protocol.subscribe('topic_name'):
    # Do something with the message here!

# Publish a message to topic
protocol.publish('topic_name', 'Message')
```

## Tests

The tests currently use a MockGooglePubsub adapter to test code functionality rather than GooglePubsub connection.
