from jsonschema import RefResolver
from jsonschema.validators import validators
from pubsub.common import Resolver

from rapidjson import (
    Validator as _RapidJsonValidator,
    ValidationError as _RapidJsonValidationError,
)


class ValidationError(Exception):
    def __init__(self, errors=None, *args, **kwargs):
        self.errors = errors
        super().__init__(*args, **kwargs)


class SchemaError(Exception):
    def __init__(
        self, msg="No schema or schema uri provided", *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class BaseValidator(object):
    def validate(self, message, schema):
        raise NotImplementedError()


class JsonSchemaValidator(BaseValidator):
    def __init__(self, resolver=None, draft_version="draft7"):
        self.resolver = resolver or RefResolver(
            base_uri="", referrer="", cache_remote=True
        )
        self.draft_version = draft_version

    def validate(self, message, schema=None, schema_uri=None):
        if schema is None and schema_uri is None:
            raise SchemaError()

        if schema is None:
            schema = self.resolver.resolve_from_url(schema_uri)

        validator = validators.get(self.draft_version)(
            schema, resolver=self.resolver
        )
        errors = [err for err in validator.iter_errors(message)]

        if errors:
            raise ValidationError(errors=errors)

        return True


class RapidJsonValidator(BaseValidator):
    def __init__(self, resolver=None, draft_version="draft7"):
        self.resolver = resolver or Resolver()
        self.draft_version = draft_version

    def validate(self, message, schema=None, schema_uri=None):
        if schema is None and schema_uri is None:
            raise SchemaError()

        if schema is None:
            schema = self.resolver.resolve_from_url(schema_uri)

        validator = _RapidJsonValidator(schema)
        try:
            validator(message)
        except _RapidJsonValidationError as exc:
            raise ValidationError(errors=[exc])
        except ValueError:
            raise ValidationError(errors=["Invalid JSON"])

        return True
