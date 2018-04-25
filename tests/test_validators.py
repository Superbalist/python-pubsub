from unittest import TestCase

from pubsub.validators.validator import SchemaValidator
from pubsub.validators.resolver import CachingRefResolver


class MockCache(object):
    def __init__(self):
        self.cache = dict()

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.setdefault(key, value)

    def clear(self):
        self.cache = dict()


class TestCachedRefResolver(TestCase):
    @classmethod
    def setUp(cls):
        cls.valid_message = {
            'schema': 'https://raw.githubusercontent.com/Superbalist/python-pubsub/gh-pages/examples/schema/card.json',
            'familyName': 'foo',
            'givenName': 'bar',
        }
        cls.invalid_message = {
            'schema': 'https://raw.githubusercontent.com/Superbalist/python-pubsub/gh-pages/examples/schema/card.json',
            'givenName': 'baz',
        }

        cls.schema_content = {
            '$schema':
            'http://json-schema.org/draft-06/schema#',
            'description':
            'A representation of a person, company, organization, or place',
            'properties': {
                'additionalName': {
                    'items': {
                        'type': 'string'
                    },
                    'type': 'array'
                },
                'adr': {
                    '$ref': 'http://json-schema.org/address'
                },
                'bday': {
                    'format': 'date',
                    'type': 'string'
                },
                'email': {
                    'properties': {
                        'type': {
                            'type': 'string'
                        },
                        'value': {
                            'format': 'email',
                            'type': 'string'
                        }
                    },
                    'type': 'object'
                },
                'familyName': {
                    'type': 'string'
                },
                'fn': {
                    'description': 'Formatted Name',
                    'type': 'string'
                },
                'geo': {
                    '$ref': 'http://json-schema.org/geo'
                },
                'givenName': {
                    'type': 'string'
                },
                'honorificPrefix': {
                    'items': {
                        'type': 'string'
                    },
                    'type': 'array'
                },
                'honorificSuffix': {
                    'items': {
                        'type': 'string'
                    },
                    'type': 'array'
                },
                'logo': {
                    'type': 'string'
                },
                'nickname': {
                    'type': 'string'
                },
                'org': {
                    'properties': {
                        'organizationName': {
                            'type': 'string'
                        },
                        'organizationUnit': {
                            'type': 'string'
                        }
                    },
                    'type': 'object'
                },
                'photo': {
                    'type': 'string'
                },
                'role': {
                    'type': 'string'
                },
                'sound': {
                    'type': 'string'
                },
                'tel': {
                    'properties': {
                        'type': {
                            'type': 'string'
                        },
                        'value': {
                            'format': 'phone',
                            'type': 'string'
                        }
                    },
                    'type': 'object'
                },
                'title': {
                    'type': 'string'
                },
                'tz': {
                    'type': 'string'
                },
                'url': {
                    'format': 'uri',
                    'type': 'string'
                }
            },
            'required': ['familyName', 'givenName'],
            'type':
            'object'
        }

        cls.cache = MockCache()
        cls.validator = SchemaValidator(
            resolver=CachingRefResolver(
                cache=cls.cache,
                base_uri='',
                referrer=''))

    def tearDown(self):
        self.cache.clear()

    def test_cache_hit(self):
        self.cache.set(self.valid_message.get('schema'), self.schema_content)
        self.validator.validate_message(self.valid_message)

    def test_cache_miss(self):
        self.cache.clear()
        self.validator.validate_message(self.valid_message)
