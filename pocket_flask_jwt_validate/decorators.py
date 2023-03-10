import jwt
import os
from collections.abc import Callable
from flask import request
from werkzeug.exceptions import Unauthorized


def _format_keystring_as_pem(key_string: str):
    return f"""-----BEGIN PUBLIC KEY-----
{key_string}
-----END PUBLIC KEY-----"""


PUBLIC_KEY = os.environ.get('AUTH_PUBLIC_KEY')


def jwt_required(public_key=PUBLIC_KEY) -> Callable:
    def wrapper(func: Callable) -> Callable:
        def inner(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            if auth_token:
                pk = _format_keystring_as_pem(public_key)
                try:
                    decoded = jwt.decode(auth_token, key=pk, algorithms=["ES256"])
                    # here we can provide some info from JWT to view function if required
                except jwt.exceptions.PyJWTError as e:
                    raise Unauthorized()
                except Exception as e:
                    raise Unauthorized()
                # if all is fine - we'll call a view function
            else:
                raise Unauthorized()
            return func(*args, **kwargs)
        return inner
    return wrapper
