from functools import wraps
from requests.models import Response
from typing import Any, Callable, Optional

from ._utilities import urljoin

_requests_kwargs: list[str] = [
    "method",
    "url",
    "params",
    "data",
    "headers",
    "cookies",
    "files",
    "auth",
    "timeout",
    "allow_redirects",
    "proxies",
    "hooks",
    "stream",
    "verify",
    "cert",
    "json",
]


def _consume_url(*args) -> Optional[tuple[str, list]]:
    """Consume *args and return a tuple with (url, remaining_args); presuming that the first positional param
    in *args is a path for a url.
    :param *args: positional arguments from a function/method"""
    if args and len(args) > 0:
        return (args[0], [*args[1:]])


def _consume_request_kwargs(**kwargs) -> tuple(dict, dict):
    """Parses out any keyword arguments that belong to requests.Session calls from those
    that belong to a decorated request function and returns a tuple object with seperate kwarg dicts.
    :param **kwargs: kwargs from a function decorated by 'request'"""
    func_kwargs, rqst_kwargs = {}, {}

    for k, v in kwargs.items():
        if k in _requests_kwargs:
            rqst_kwargs[k] = v
        else:
            func_kwargs[k] = v

    return (rqst_kwargs, func_kwargs)


def _consume_param_kwargs(param_keys: list[str], **kwargs) -> tuple[dict, dict]:
    """Consumes kwargs that are to be used as params, returns a tuple with
    the params kwarg dict in the first index position and the remaining kwargs in the
    second index position.
    :param params: a list of strings representing the key names of params
    :param **kwargs: kwargs to consume"""
    params, remnants = {}, {}

    for k, v in kwargs.items():
        if k in param_keys:
            params[k] = v
        else:
            remnants[k] = v

    return (params, remnants)


def _consume_status_kwargs(self, **kwargs) -> tuple[list[int], list[int]]:
    """Parse a function's keyword arguments for any ignorable/retry status code lists.
    :param **kwargs: kwargs from a function"""
    ignore = [*kwargs.get("ignore_statuses", []), *self.HTTP_IGNORE_STATUS_ERR]
    retry = [*kwargs.get("retry_statuses", []), *self.HTTP_RETRY_STATUS_LIST]

    return (ignore, retry)


def file_upload(field: tuple[str, list]) -> Callable:
    """Decorator for internal methods that have a file upload to process.
    :param field: a tuple with the name of the field where the upload is processed to in the
                  first index position, and a list of other attribute key names to include in the
                  'params' kwarg in the second index position"""

    def wrap_function(fn: Callable) -> Callable:
        """Wraps the method being used ot perform the POST method.
        :param fn: the callable being decorated"""

        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Response:
            """Wrapper to perform actions on the wrapped function from 'wrap_function'"""
            fieldname, param_keys = field  # get the string representation of the path
            params, kwargs = _consume_param_kwargs(param_keys=param_keys, **kwargs)
            file = kwargs.get(fieldname)  # for opening the file
            del kwargs[fieldname]  # don't need this in params anymore

            # hardcoded mode of 'read, binary'; a binary object is expected by the API
            with open(file, "rb") as f:
                params["files"] = f
                kwargs.setdefault("params", params)
                response = self.post(*args, **kwargs)
                return response

        return wrap_actions

    return wrap_function


def request(method: str) -> Callable:
    """Decorator for internal methods that require a requests.Session method call.
    :param method: the REST method action to perform, for example 'delete', 'get', 'patch', 'post', 'put'"""

    def wrap_function(fn: Callable) -> Callable:
        """This wraps the method performing the REST action; for example self.get(url) is decorated with '@request',
        so the self.get() method is being wrapped."""

        @wraps(fn)  # keep docstrings, and arguments from original function
        def wrap_actions(self, *args, **kwargs) -> Response:
            """Wrapper to perform actions on the wrapped function from 'wrap_function'."""
            # pre-process arguments, consuming args and kwargs
            rqst_kwargs, func_kwargs = _consume_request_kwargs(**kwargs)
            ignore, retry = _consume_status_kwargs(**func_kwargs)
            url_path, rqst_args = _consume_url(*args)
            url = urljoin(url_path, base_url=self.base_url)

            # modify the session with some values
            rqst_kwargs.setdefault("timeout", (self.HTTP_CONNECT_TIMEOUT, self.HTTP_READ_TIMEOUT))
            self.session.mount("https://", self._session_retry(retry))

            # now perform the request
            response = self.session.request(method, url, *rqst_args, **rqst_kwargs)

            # handle any exceptions that should raise a HTTP status exception, except when it's
            # ok to safely ignore those errors
            if response.status_code not in ignore:
                response.raise_for_status()

            return response  # return the object

        return wrap_actions

    return wrap_function


def paginate(fn: Callable) -> Callable:
    """Decorator for API methods that require paginating a response from a 'get' request.
    :param fn: callable"""

    @wraps(fn)
    def wrapper_for_paginating(self, *args, **kwargs):
        """Performs the pagination."""
        has_more = True
        params, kwargs = _consume_param_kwargs(param_keys=["limit", "starting_after"])
        params.setdefault("limit", 100)
        params.setdefault("starting_after", 0)
        kwargs["params"] = params

        while has_more:
            response = self.get(*args, **kwargs)
            json_data = response.json()
            objects = json_data.get("data", [])

            if objects:
                for obj in objects:
                    yield obj

                kwargs["params"]["starting_after"] = objects[-1].get("id")
            has_more = json_data.get("has_more", False)

    return wrapper_for_paginating


def url_suffixes(suffix: str, add_kwarg_vals_to_url: Optional[list] = []):
    """Decorator for adding an additional suffix to the base url and endpoint, along with
    and additional values from kwargs provided to the API method, for example, adding 'bluetooth'
    to 'https://a.simplemdm.com/api/v1/devices/{id}' to become:
        'https://a.simplemdm.com/api/v1/devices/{id}/bluetooth'
    Items in the 'add_kwargs_vals_to_url' are processed in order, and any matching kwarg value is
    then added to the URL, for example, turning url_suffixes('custom_attribute_values', ["attr_name"])
    into:
        https://a.simplemdm.com/api/v1/devices/{id}/custom_attribute_values/{attr_name}"""

    def wrapper_for_suffixing(fn: Callable) -> Callable:
        """Performs the suffix actions."""

        @wraps(fn)
        def wrap_action(self, *args, **kwargs) -> Callable:
            """This wraps the method and returns the function with a new set of *args"""
            try:
                new_path = f"{args[0]}/{suffix}"
            except IndexError:
                # this may have unintended consequences as it is untested if this is the appropriate action to take
                raise Exception(f"Error: could not append {suffix!r} to URL")
            finally:
                if add_kwarg_vals_to_url:
                    kwargs_path = "/".join(kwargs.get(kv) for kv in add_kwarg_vals_to_url)
                    new_path = f"{new_path}/{kwargs_path}"

                args = [new_path, *args[1:]] if args else [new_path]

                return fn(*args, **kwargs)

        return wrap_action

    return wrapper_for_suffixing
