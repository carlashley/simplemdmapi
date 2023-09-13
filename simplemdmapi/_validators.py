from functools import wraps
from typing import Callable


def validate_pin(param: str, length: int):
    """Decorator for performing a validation on the wrapped API method.
    :param param: the name of the parameter to validate length for
    :param length: expected character length"""

    def wrapper_a(fn: Callable):
        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            """Wrapper that is wrapped around the callable object that has been decorated.
            :params *args: positional arguments that are paramters of the decorated function
            :params **kwargs: positional keyword arguments that are parameters of the decorated
                              function"""
            if not len(kwargs.get(param)) == length:
                raise ValueError(f"{fn.__name__}() option for {param!r} does not meet length requirement of {length}")

            if not all(n.isdigit() for n in kwargs.get(param)):
                raise ValueError(f"{fn.__name__}() option for {param!r} contains non-numeric characters")

        return wrapper_b

    return wrapper_a
