from functools import wraps
from typing import Callable


def params_or_required(param_keys: list[str]):
    """Decorator for performing a validation on the wrapped API method.
    :param param_keys: list of parameter names that need to be validated where any one of are required"""

    def wrapper_a(fn: Callable):
        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            """Wrapper that is wrapped around the callable object that has been decorated.
            :params *args: positional arguments that are paramters of the decorated function
            :params **kwargs: positional keyword arguments that are parameters of the decorated
                              function"""
            if not any(pk in kwargs for pk in param_keys):
                raise AttributeError(f"Error: {fn.__name__!r} requires one or more parameters: {param_keys}")

        return wrapper_b

    return wrapper_a


def pin_length(param: str, length: int):
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
            if not kwargs.get(param):
                raise AttributeError(f"Error: {fn.__name__!r} requires the parameter: {param}")
            else:
                if not len(kwargs.get(param)) == length:
                    raise ValueError(f"Error: {fn.__name__!r} parameter {param!r} must be {length} characters long")

        return wrapper_b

    return wrapper_a


def all_digits(param: str):
    """Decorator for performing a validation on the wrapped API method.
    :param param: the name of the parameter to validate all characters are digits"""

    def wrapper_a(fn: Callable):
        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            """Wrapper that is wrapped around the callable object that has been decorated.
            :params *args: positional arguments that are paramters of the decorated function
            :params **kwargs: positional keyword arguments that are parameters of the decorated
                              function"""
            if not all(c.isdigit() for c in kwargs.get(param)):
                raise ValueError(f"Error: {fn.__name__!r} parameter value is not all digits")

        return wrapper_b

    return wrapper_a


def validate_param_opts(param_opts: list[tuple[str, list[str]]]):
    """Decorator for performing a validation on the wrapped API method.
    :param param: the name of the parameter to validate all characters are digits"""

    def wrapper_a(fn: Callable):
        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            """Wrapper that is wrapped around the callable object that has been decorated.
            :params *args: positional arguments that are paramters of the decorated function
            :params **kwargs: positional keyword arguments that are parameters of the decorated
                              function"""
            for param, options in param_opts:
                param_value = kwargs.get(param)

                if param in kwargs and param_value not in options:
                    raise ValueError(
                        f"Error: {fn.__name__!r} parameter {param!r} has invalid option {param_value!r}; choose"
                        f" from {options}"
                    )

        return wrapper_b

    return wrapper_a
