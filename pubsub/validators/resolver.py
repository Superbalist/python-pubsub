from cachetools import TTLCache

from jsonschema import RefResolver


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


class CachingRefResolver(RefResolver):
    """
    Reference resolver that allows for caching of resolved documents.

    Args:
        cache: SimpleCache, or optionally provided cache object for the resolved documents.

    Examples:

        >>> validator = SchemaValidator(
        >>>                 resolver=CachingRefResolver(
        >>>                     cache=SimpleCache(maxsize=1024, ttl=300),
        >>>                     base_uri='',
        >>>                     referrer=''))

    """
    def __init__(self, cache=None, *args, **kwargs):
        self.cache = cache or SimpleCache()
        super(CachingRefResolver, self).__init__(*args, **kwargs)

    def resolve_from_url(self, url):
        document = self.cache.get(url)
        if document is None:
            document = super(CachingRefResolver, self).resolve_from_url(url)
            self.cache.set(url, document)

        return document
