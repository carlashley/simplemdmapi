import errno
import os

from functools import wraps
from itertools import combinations
from pathlib import Path
from typing import Callable

from .utils import pkg_is_signed


class PackageNotSigned(Exception):
    """Package not Signed Exception handling."""
    pass


def _generate_bad_combinations(params: tuple) -> list[str]:
    """Generate all possible bad combinations of paramters.
    :param params: tuple of list of strings or list of strings representing the name of each parameter that
                   can't be combined"""
    result = []

    for p in params:
        _min, _max = len(p) - 1, len(p)
        cmbns = [*[[c for c in combinations(p, n)] for n in range(_min, _max)][0]]
        result.extend(cmbns)

    if result:
        return result


def validate_required(kwargs: dict, req_params: list, fn_name: str) -> None:
    """Check kwargs for required parameters.
    :param kwargs: dictionary object of kwargs
    :param req_params: list of required params
    :param fn_name: function name for exceptions"""
    for req_param in req_params:
        if req_param not in kwargs:
            raise TypeError(f"{fn_name}() missing required keyword-only parameter: {req_param!r}")


def validate_any(kwargs: dict, any_params: list, fn_name: str) -> None:
    """Check kwargs for any paramters that are optional but where one or more must be provided.
    :param kwargs: dictionary object of kwargs
    :param any_params: list of any optional 'required' params
    :param fn_name: function name for exceptions"""
    if not any(any_param in kwargs for any_param in any_params):
        raise TypeError(f"{fn_name}() missing at least one optional keyword-only parameter: {any_params}")


def validate_incompatible(kwargs: dict, inc_params: list, fn_name: str) -> None:
    """Check kwargs for any paramters that are incompatible with other parameters.
    :param kwargs: dictionary object of kwargs
    :param inc_params: list of any incompatible parameters
    :param fn_name: function name for exceptions"""
    bad_combos = _generate_bad_combinations(inc_params)

    for kwarg in kwargs:
        for combo in bad_combos:
            for bad_kwarg in combo:
                if bad_kwarg in kwargs and kwarg in inc_params and not bad_kwarg == kwarg:
                    raise AttributeError(f"{fn_name}() {bad_kwarg!r} not permitted with {kwarg!r}")


def validate_param_opts(kwargs: dict, val_params: dict, fn_name: str) -> None:
    """Validate values for parameters that only accept specific values.
    :param kwargs: dictionary object of kwargs
    :param val_params: dict of any value parameters to check, {"param": ["valid", "values"]}
    :param fn_name: function name for exceptions"""
    for param, values in val_params.items():
        value = kwargs.get(param)

        if value and value not in values:
            err = f"{fn_name}() unexpected value {value!r} for {param!r}, expecting one of: {values}"
            raise ValueError(err)


def validate_pin(param: str, length: int) -> None:
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
            _param = kwargs.get("params", {}).get(param)

            if _param:
                if not len(_param) == length:
                    err = f"{fn.__name__}() option for {param!r} does not meet length requirement of {length}"
                    raise ValueError(err)

                if not all(n.isdigit() for n in kwargs.get("params", {}).get(param)):
                    raise ValueError(f"{fn.__name__}() option for {param!r} contains non-numeric characters")

        return wrapper_b

    return wrapper_a


def validate_package(pkg: Path, fn_name: str) -> None:
    """Validate a package installer file is signed.
    :param pkg: path object
    :param fn_name: function name for exceptions"""
    if not pkg.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(pkg))
    else:
        if not pkg_is_signed(pkg):
            raise PackageNotSigned(f"{fn_name}() {str(pkg)!r} is not signed, only signed packages can be uploaded.")
