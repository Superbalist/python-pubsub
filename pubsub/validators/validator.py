import re

from jsonschema import Draft4Validator, RefResolver, ValidationError as SchemaValidationError


class ValidationError(Exception):
    def __init__(self, errors=None, *args, **kwargs):
        self.errors = errors
        super(ValidationError, self).__init__(*args, **kwargs)


class BaseValidator(object):
    """
    Validates pubsub messages against specified schema
    """
    def validate_message(self, message):
        raise NotImplementedError()


class SchemaValidator(BaseValidator):
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
        schema = RefResolver('', '').resolve_remote(schema_uri)
        errors = []
        for error in Draft4Validator(schema).iter_errors(message):
            errors.append(error)
        if errors:
            raise ValidationError(errors=errors)


class EmptyValidator(BaseValidator):
    """
    Validates that message is not None
    """

    def validate_message(self, message):
        return message != ''
