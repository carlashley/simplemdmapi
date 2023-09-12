from functools import wraps
from itertools import combinations
from typing import Callable


def all_params(params: list[str]) -> Callable:
    """Decorator for internal methods that need all parameters. This should be decorated on a function before
    the 'param_kwargs' decorator."""

    def wrap_function(fn: Callable) -> Callable:
        """Wraps the method that has the params to parse.
        :param fn: the callable being decorated"""

        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Callable:
            """Wrapper to perform actions on the wrapped fucntion from 'wrap_function'."""
            if not all(p in kwargs for p in params):
                raise TypeError(f"{fn.__name__}() missing required keyword-only arguments: {params}")

        return wrap_actions

    return wrap_function


def any_params(params: list[str]) -> Callable:
    """Decorator for internal methods that need at least one parameter. This should be decorated on a function before
    the 'param_kwargs' decorator."""

    def wrap_function(fn: Callable) -> Callable:
        """Wraps the method that has the params to parse.
        :param fn: the callable being decorated"""

        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Callable:
            """Wrapper to perform actions on the wrapped fucntion from 'wrap_function'."""
            if not any(p in kwargs for p in params):
                raise TypeError(f"{fn.__name__}() missing at least one required keyword-only argument: {params}")

        return wrap_actions

    return wrap_function


def bad_combo_params(good_param: str, bad_params: list[str]) -> Callable:
    """Decorator for internal methods that cannot have any combination of the parameters. This should be decorated on
    a function before the 'param_kwargs' decorator.
    :param good_param: the good parameter to test for existence with other parameters
    :param bad_params: the bad paramters that cannot be used with the good parameter"""
    def wrap_function(fn: Callable) -> Callable:
        """Wraps the method that has the params to parse.
        :param fn: the callable being decorated"""

        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Callable:
            """Wrapper to perform actions on the wrapped fucntion from 'wrap_function'."""
            # generate all possible combinations of params, exclude one param because it's the one being tested
            if good_param in kwargs and any((bp in kwargs and not bp == good_param) for bp in bad_params):
                bad = [bp for bp in bad_params if bp in kwargs and not bp == good_param]
                raise AttributeError(f"{wrap_actions.__name__}() {good_param!r} cannot be used with {bad}")

        return wrap_actions

    return wrap_function


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
                    raise ValueError(f"{fn.__name__}() invalid option for {param!r}, choose from {options}")

        return wrapper_b

    return wrapper_a
