from unittest.mock import MagicMock
from pytest import raises

from pubsub.validators import (
    JsonSchemaValidator,
    RapidJsonValidator,
    ValidationError,
    BaseValidator,
    SchemaError,
)

from tests._common import (
    SCHEMA_PAYLOAD,
    PERSON_PAYLOAD,
    NOT_PERSON_PAYLOAD,
    SCHEMA_OBJ,
    PERSON_OBJ,
    NOT_PERSON_OBJ,
    BROKEN_PAYLOAD,
    SCHEMA_URI,
)


def test_base_validator():
    v = BaseValidator()
    with raises(NotImplementedError):
        v.validate(PERSON_OBJ, SCHEMA_OBJ)


def test_jsonschema_validator():
    v = JsonSchemaValidator()
    res = v.validate(message=PERSON_OBJ, schema=SCHEMA_OBJ)
    assert res is True

    v.resolver.resolve_from_url = MagicMock(return_value=SCHEMA_OBJ)
    v.validate(message=PERSON_OBJ, schema_uri=SCHEMA_URI)

    with raises(ValidationError):
        v.validate(message=NOT_PERSON_OBJ, schema=SCHEMA_OBJ)

    with raises(SchemaError):
        v.validate(message=PERSON_OBJ)

    with raises(ValidationError):
        v.validate(BROKEN_PAYLOAD, schema=SCHEMA_OBJ)


def test_rapidjson_validator():
    v = RapidJsonValidator()
    res = v.validate(message=PERSON_PAYLOAD, schema=SCHEMA_PAYLOAD)
    assert res is True

    v.resolver.resolve_from_url = MagicMock(return_value=SCHEMA_PAYLOAD)
    v.validate(message=PERSON_PAYLOAD, schema_uri=SCHEMA_URI)

    with raises(ValidationError):
        v.validate(message=NOT_PERSON_PAYLOAD, schema=SCHEMA_PAYLOAD)

    with raises(SchemaError):
        v.validate(message=PERSON_PAYLOAD)

    with raises(ValidationError):
        v.validate(BROKEN_PAYLOAD, schema=SCHEMA_PAYLOAD)
