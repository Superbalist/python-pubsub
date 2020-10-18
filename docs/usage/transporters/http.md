# Redis usage
## Publish
```python
from pubsub.transporters.transporters import HTTPTransport

payload = """
{
  "latitude": -48.876667,
  "longitude": -123.393333
}
"""
channel = "ping"

t = HTTPTransport()
t.publish(channel, payload)
```