# Google 
## Publish
```python
from pubsub.transporters.transporters import GooglePubsubTransport


t = GooglePubsubTransport(project="sandbox")

payload = """
{
    "cart": {
        "_id": 625371,
        "items": [
            {
                "sku": "GCK09MJAH",
                "qty": 14
            }
        ]
    }
}
"""

t.publish("cart", payload)
```

## Subscribe
```python
from pubsub.transporters.transporters import GooglePubsubTransport

def callback(msg):
    print(msg)

t = GooglePubsubTransport(project="sandbox")

t.subscribe("test", callback=callback)
```