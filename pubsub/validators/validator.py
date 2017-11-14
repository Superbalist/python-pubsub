import re
import jsonschema
from jsonschema import ValidationError


class SchemaValidator():
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
        if len(matches) >= 1:
            schema = jsonschema.RefResolver('', '').resolve_remote(schema_uri)
            jsonschema.validate(message, schema)
        else:
            raise ValidationError('Incorrect schema uri')


class EmptyValidator():
    """
    Validates that message is not None
    """

    def validate_message(self, message):
        return True if (message != '') else False
