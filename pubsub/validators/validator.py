import re

from jsonschema import Draft4Validator, RefResolver


class ValidationError(Exception):
    def __init__(self, *args, errors=None, **kwargs):
        self.errors = errors
        super(ValidationError, self).__init__(*args, **kwargs)


class BaseValidator(object):
    """
    Validates pubsub messages against specified schema
    """
    publish_errors = False
    errors_topic = None
    errors_schema = None

    def __init__(self, publish_errors=False, errors_topic=None, errors_schema=None):
        self.publish_errors = publish_errors
        if publish_errors and not errors_topic:
            raise ValueError('errors_topic needs to be set if publish_errors is turned on')
        if publish_errors and not errors_schema:
            raise ValueError('errors_schema needs to be set if publish_errors is turned on')

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
        matches = re.findall(r'(.+)://(.+/)?events/(.+)/(.+)/(.+)\.json', schema_uri)
        if len(matches) < 1:
            raise ValidationError('Incorrect schema uri')
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
