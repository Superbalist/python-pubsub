import re

from cachetools import TTLCache
from jsonschema import Draft4Validator, RefResolver, ValidationError as SchemaValidationError


class ValidationError(Exception):
    def __init__(self, errors=None, *args, **kwargs):
        self.errors = errors
        super(ValidationError, self).__init__(*args, **kwargs)


class SimpleCache(TTLCache):
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def set(self, key, value):
        self.__setitem__(key, value)


class CachingRefResolver(RefResolver):
    def __init__(self, cache=None, *args, **kwargs):
        if cache is None:
            cache = SimpleCache(maxsize=1024, ttl=300)
        self.cache = cache
        super(CachingRefResolver, self).__init__(*args, **kwargs)

    def resolve_from_url(self, url):
        document = self.cache.get(url)
        if document is None:
            print(('miss', url))
            document = super(CachingRefResolver, self).resolve_from_url(url)
            self.cache.set(url, document)
        else:
            print(('hit', url))

        return document


class BaseValidator(object):
    """
    Validates pubsub messages against specified schema
    """
    def validate_message(self, message):
        raise NotImplementedError()


class SchemaValidator(BaseValidator):
    def __init__(self, resolver=None):
        if resolver is None:
            resolver = RefResolver('', '')
        self.resolver = resolver

    """
    Validates pubsub messages against specified schema
    """
    def validate_message(self, message):
        try:
            message.get('schema', None)
        except ValueError:
            raise ValueError('Message must contain a schema!')
        except AttributeError:
            raise AttributeError('Message must be json')
        schema_uri = message.get('schema', '')
        matches = re.findall(r'(.+)://(.+/)?(.+)\.json', schema_uri)
        if len(matches) < 1:
            raise SchemaValidationError('Incorrect schema uri: {}'.format(schema_uri))
        schema = self.resolver.resolve_from_url(schema_uri)

        errors = []
        for error in Draft4Validator(schema, resolver=self.resolver).iter_errors(message):
            errors.append(error)
        if errors:
            raise ValidationError(errors=errors)


class EmptyValidator(BaseValidator):
    """
    Validates that message is not None
    """

    def validate_message(self, message):
        return message != ''
