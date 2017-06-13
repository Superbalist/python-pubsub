#!/usr/bin/env python

from pubsub.protocol import Protocol
from pubsub.adapters.googlecloud import GooglePubsub
from pubsub.serializers.serializer import JSONSerializer
from pubsub.validators.validator import SchemaValidator

p = Protocol(adapter=GooglePubsub(), serializer=JSONSerializer(), validator=SchemaValidator())
valid = {
  "schema": "http://schema.superbalist.com/events/shopping_cart/created/1.0.json",
  "meta": {
    "date": "2017-02-01T12:39:12+00:00",
    "uuid": "5AB2ABB6-8617-4DDA-81F7-DD47D5882B19",
    "service": "api",
    "hostname": "superbalist-api-1935885982-59xk1"
  },
  "shopping_cart": {
    "id": 1070486,
    "is_expired": False,
    "is_restorable": True,
    "user": {
      "id": 2,
      "email": "matthew@superbalist.com",
      "first_name": "Matthew",
      "last_name": "Goslett"
    },
    "items": [

    ]
  }
}
invalid = {'blah': 'blah'}

for m in valid, invalid:
  try:
    p.publish('test_cart_abandonment', m)
  except:
    print("Failed")
