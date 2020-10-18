# Google 

```python
from pubsub import BaseProtocol, Message, GooglePubsubTransport, JsonSerializer


PROJECT_ID = "my-sandbox"
CHANNEL_NAME = "test"
SUBSCRIBER_NAME = "pubsub-test"


class MySubscriber(BaseProtocol):
    def handle_message(self, message: Message):
        # do something.
        print(repr(message))


t = GooglePubsubTransport(project=PROJECT_ID, name=SUBSCRIBER_NAME)
s = JsonSerializer()
p = MySubscriber(
    transport=t,
    serializer=s,
    wrap_in_message=True,
    raise_exceptions=False
)
p.subscribe(CHANNEL_NAME, create=True, delete=False)
```