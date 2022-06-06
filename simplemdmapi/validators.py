"""Validator functions for API queries."""
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Union


class ParamException(Exception):
    """Raise exceptions for parameters."""
    pass


class UploadException(Exception):
    """Raise exceptions for file uplaods."""
    pass


def parse_kwargs(kwargs: Dict[Any, Any]) -> Dict[Any, Any]:
    """Pre-parse kwarg dictionary to remove keys that are not
    standard 'requests.request' API params."""
    requests_api_args = ["method",
                         "url",
                         "params",
                         "data",
                         "json",
                         "headers",
                         "cookies",
                         "files",
                         "auth",
                         "timeout",
                         "allow_redirects",
                         "proxies",
                         "verify",
                         "stream",
                         "cert"]

    # work on a copy of kwargs because we're modifying it
    for k, _ in kwargs.copy().items():
        if k not in requests_api_args:
            try:
                del kwargs[k]
            except KeyError:
                pass

    return kwargs


def required_params(params: List[Any], reqd_params: List[Any]) -> None:
    """Validated required parameters exist"""
    missing_params: List[str] = list()

    for param in reqd_params:
        if param not in params:
            missing_params.append(param)

    if missing_params:
        raise ParamException(f"Error: Missing paramters {missing_params}: Required parameters are {reqd_params}")


def validate_file_exts(files: Union[List[str], str], valid_file_exts: List[str]) -> None:
    """Validate file extensions before uploading.
    :param files: list of file paths or a single file path as a string/strings
    :param valid_file_exts: list of file extensions as a string, include the '.'"""
    invalid_files: List[str] = list()

    if isinstance(files, list):
        for f in files:
            if Path(f).suffix not in valid_file_exts:
                invalid_files.append(f)
    else:
        if Path(files).suffix not in valid_file_exts:
            invalid_files.append(files)

    if invalid_files:
        raise UploadException(f"Error: invalid file extensions for {invalid_files}: Valid file extensions: {valid_file_exts}")


def validate_params(params: Dict[Any, Any], valid_params: List[Any]) -> None:
    """Check a supplied list of parameters against a list of valid parameters.
    :param params: dictionary of parameters supplied to a method
    :param valid_params: list of valid parameter names to check against"""
    invalid_params: List[str] = list()

    for param in params:
        if param not in valid_params:
            invalid_params.append(param)

    if invalid_params:
        raise ParamException(f"Invalid parameters: {invalid_params}; Valid parameters: {valid_params}")


def validate_unique_params(params: Dict[Any, Any], uniq_params: List[Any]) -> None:
    """Validate parameters are a unique combination.
    :param params: dictionary of parameters to check for uniqueness
    :param uniq_params: list of parameters that cannot co-exist"""
    possible_combinations: List[Any] = list()
    params_as_tuple = tuple(params)

    for n in range(1, len(uniq_params) + 1):
        possible_combinations.extend(list(combinations(uniq_params, n)))

    if len(params_as_tuple) > 1 and params_as_tuple in possible_combinations:
        raise ParamException(f"Error: Only unique parameters can be supplied, use one of: {uniq_params}")
