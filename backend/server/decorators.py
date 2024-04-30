from functools import wraps
from flask import request, abort 

from jsonschema import validators
from jsonschema.exceptions import SchemaError, ValidationError

from server.schemas import SCHEMA

def validate(schema: SCHEMA):
    """Validates the request JSON data agains schema 
    and aborts with wrong/invalid data.

    Aborts with a 400 Error if Validation error is 
    triggered or no JSON data is supplied. 

    Args:
        schema (SCHEMA): A JSON schema.

    Returns:
        _type_: The result of func.
    """
    def validateDecorator(func):
        """The actual decorator for validating JSON data.

        This method needs to be wrapped by another method
        because the schema can not be supplied otherwise.

        Args:
            func (_type_): A function processing a request.

        Returns:
            _type_: The result of func.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Validates JSON data based on schema and 
            aborts in case of errors.

            Aborts:
                400: Invalid input data.
                500: Invalid schema.

            Returns:
                _type_: The result of func
            """
            if not request.is_json:
                abort(400)

            data = request.get_json()
            try:
                validators.validate(data, schema)
            except SchemaError:
                abort(500)
            except ValidationError as val_err:
                abort(400, val_err)
            else:
                return func(*args, **kwargs)
        return wrapper
    return validateDecorator
