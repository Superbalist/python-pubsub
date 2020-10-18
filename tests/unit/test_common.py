import respx

from pubsub.common import SimpleCache, Resolver
from tests._common import EVENT_PAYLOAD, EVENT_OBJ


def test_simplecache():
    c = SimpleCache()
    assert isinstance(c, SimpleCache)

    c.set("foo", {"foo": "moo"})
    v = c.get("foo")
    assert isinstance(v, dict)
    assert v["foo"] == "moo"

    v = c.get("coo", 7623)
    assert v == 7623

    v = c.get("loo")
    assert v is None


@respx.mock
def test_resolver():
    cache = SimpleCache()
    r = Resolver(store=cache)
    uri = "https://example.com/json-schema/event.json"

    request = respx.get(uri, status_code=200, content=EVENT_PAYLOAD)
    response = r.resolve_from_url(uri)
    assert response == EVENT_OBJ
    assert request.called

    request = respx.get(uri, status_code=200, content=EVENT_PAYLOAD)
    response = r.resolve_from_url(uri)
    assert response == EVENT_OBJ
    assert not request.called
