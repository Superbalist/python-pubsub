import httpx
from cachetools import TTLCache


class SimpleCache(TTLCache):
    """
    Wrapper around the cachetools.TTLCache to provide get and set methods
    """

    def __init__(self, maxsize=1024, ttl=300, *args, **kwargs):
        super(SimpleCache, self).__init__(maxsize, ttl, *args, **kwargs)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def set(self, key, value):
        self.__setitem__(key, value)


class Resolver:
    store: object

    def __init__(self, store: object = SimpleCache()):
        self.store = store

    def resolve_from_url(self, uri: str):
        return self.store.get(uri, self.resolve_remote(uri))

    def resolve_remote(self, uri: str):
        with httpx.Client() as client:
            response = client.get(uri).json()

        self.store.set(uri, response)

        return response
