# python-pubsub

## Adapters

* GoogleCloudAdapter
* KafkaAdapter
* RedisAdapter

## Usage

* `pip install .` to run setup.py and allow you to import the package
* `from pubsub import GoogleCloudAdapter, KafkaAdapter, RedisAdapter`
* create an instance of an adapter, eg. `c = GoogleCloudAdapter`

All adapters have subscribe and publish methods

```
def publish(self, channel, message, **kwargs):
```
Publish has no return type

```
def subscribe(self, channel, handler=lambda x: x, **kwargs):
```
Subscribe return a generator which yields the message to the handler

## Tests

Currently only works with GoogleCloudAdapter

* setUp

Creates an adapter instance and threading event

* Many-To-One

Sends many messages(unique) to one subscriber instance

* One-To-Many

TODO

* tearDown

Deletes the subscriptions and topics created during the test
