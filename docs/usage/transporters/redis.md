# Redis usage
## Publish
```python
from pubsub.transporters.transporters import RedisTransport

payload = """
{
  "latitude": -48.876667,
  "longitude": -123.393333
}
"""
channel = "ping"

t = RedisTransport()
t.publish(channel, payload)
```

## Subscribe
```python
from pubsub.transporters.transporters import RedisTransport

t = RedisTransport()

def callback(message):
    print(message)

t.subscribe("test", callback)
```

## Pattern subscribe
```python
from pubsub.transporters.transporters import RedisTransport

t = RedisTransport()

def callback(message):
    print(message)

t.pattern_subscribe("fo*")
```
