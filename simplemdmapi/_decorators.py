from functools import wraps
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response
from typing import Callable, Optional

from ._utilities import urljoin
from ._validators import _any_params_check, _incompatible_params_check, _required_params_check, _validate_param_options

# used for tracking the kwargs that get passed to 'requests.Session.request'
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


def _consume_request_kwargs(**kwargs) -> tuple[dict, dict]:
    """Parses out any keyword arguments that belong to 'requests.Session' calls from those
    that belong to a decorated request function and returns a tuple object with seperate kwarg dicts.
    :param **kwargs: kwargs from a function decorated by 'request'"""
    func_kwargs, rqst_kwargs = {}, {}

    for k, v in kwargs.items():
        if k in _requests_kwargs:
            rqst_kwargs[k] = v
        else:
            func_kwargs[k] = v

    return (rqst_kwargs, func_kwargs)


def _consume_status_kwargs(self, **kwargs) -> tuple[list[int], list[int]]:
    """Parse function keyword arguments for any ignorable/retry status code lists.
    :param **kwargs: kwargs from a function decorated by 'request'"""
    ignore = [*kwargs.get("ignore_statuses", []), *self.HTTP_IGNORE_STATUS_ERR]
    retry = [*kwargs.get("retry_statuses", []), *self.HTTP_RETRY_STATUS_LIST]

    return (ignore, retry)


def method_params(fn) -> Callable:
    """Decorator for parsing the endpoint method parameters into a 'params' keyword argument dictionary
    object that is then parsed back in a cleaned up kwargs object.
    :param fn: the function that is being decorated; these should be SimpleMDM API methods from 'endpoints',
               such as 'endpoints.devices.Devices.create'"""

    @wraps(fn)
    def wrap_actions(self, *args, **kwargs) -> Callable:
        """Wrapper to perform actions on the wrapped fucntion from 'wrap_function'."""
        print(f"method_params args: {args}, kwargs: {kwargs}")
        _fnctn = fn.__name__
        param_conf = self._method_kwargs.get(_fnctn, {})

        # all_params = param_conf.get("all_params")
        any_params = param_conf.get("any_params")
        req_params = param_conf.get("req_params")
        inc_params = param_conf.get("inc_params")
        val_params = param_conf.get("validate")
        file_param = param_conf.get("file_param")

        # Check all required method parameters are provided
        if req_params:
            _required_params_check(kwargs, req_params, _fnctn)

        # Check any optional parameters where at least one optional parameter is required
        if any_params:
            _any_params_check(kwargs, any_params, _fnctn)

        # Check any incompatible parameter combinations
        if inc_params:
            _incompatible_params_check(kwargs, inc_params, _fnctn)

        # Validate any parameter values
        if val_params:
            _validate_param_options(kwargs, val_params, _fnctn)

        kwargs, func_kwargs = _consume_request_kwargs(**kwargs)
        file = func_kwargs.get(file_param)

        if file:
            kwargs["files"] = {file_param: file}
            del func_kwargs[file_param]  # not needed, so don't pass it and cause issues elsewhere

        # left over function kwargs get put into the 'params' key as other
        # decorators/methods rely on this existing
        kwargs["params"] = func_kwargs

        return fn(self, *args, **kwargs)

    return wrap_actions


def file_upload(fn: Callable) -> Callable:
    """Decorator for internal methods that have a file upload to process.
    :param fn: the function that is being decorated; these should be SimpleMDM API methods from 'endpoints',
               such as 'endpoints.account.PushCertificate.push_certificate_update'"""

    @wraps(fn)
    def wrap_actions(self, *args, **kwargs) -> Response:
        """Wrapper to perform actions on the wrapped function from 'wrap_function'"""
        # note, some API methods have an option to upload a file, depending on the parameters
        # passed, for example, the apps.create method can optionally upload a file to SimpleMDM,
        # so test for the existence of an upload file fieldname, and return a post response
        # either way
        file_fn = self._method_kwargs.get(fn.__name__, {}).get("file_param")

        if file_fn in kwargs.get("files", {}):
            filename = kwargs["files"].get(file_fn)

            with open(filename, "rb") as f:
                kwargs["files"][file_fn] = f
                response = self.post(*args, **kwargs)
                return response
        else:
            return self.post(*args, **kwargs)

    return wrap_actions


def request(method: str) -> Callable:
    """Decorator for internal methods that require a 'requests.Session' method call.
    :param method: the REST method action to perform, for example 'delete', 'get', 'patch', 'post', 'put'"""

    def wrap_function(fn: Callable) -> Callable:
        """This wraps the method performing the REST action; for example self.get(url) is decorated with '@request',
        so the self.get() method is being wrapped."""

        @wraps(fn)  # keep docstrings, and arguments from original function
        def wrap_actions(self, *args, **kwargs) -> Response:
            """Wrapper to perform actions on the wrapped function from 'wrap_function'."""
            ignore, retry = _consume_status_kwargs(self, **kwargs)

            if args:
                url_path, rqst_args = _consume_url(*args)
            else:
                url_path, rqst_args = None, []

            url = urljoin(self.api_vers, self.endpoint, url_path, base_url=self.BASE_URL)

            # modify the session with some values
            kwargs.setdefault("timeout", (self.HTTP_CONNECT_TIMEOUT, self.HTTP_READ_TIMEOUT))

            # modify the request headers to post JSON
            if "json" in kwargs:
                kwargs.setdefault("headers", {"Content-Type": "application/json"})

            self.session.mount(
                "https://",
                HTTPAdapter(
                    max_retries=Retry(
                        total=self.HTTP_MAX_RETRIES, status_forcelist=retry, backoff_factor=self.HTTP_RETRY_BACKOFF
                    )
                ),
            )

            if not self.dry_run:
                response = self.session.request(method, url, *rqst_args, **kwargs)

                # # handle any exceptions that should raise a HTTP status exception, except when it's
                # # ok to safely ignore those errors
                if response.status_code not in ignore:
                    response.raise_for_status()

                return response  # return the object
            else:
                print(f"perform {method!r} on {url!r} with args {rqst_args} and kwargs {kwargs}")

        return wrap_actions

    return wrap_function


def paginate(fn: Callable) -> Callable:
    """Decorator for API methods that require paginating a response from a 'get' request.
    :param fn: the method being paginated; these should be SimpleMDM API methods from 'endpoints', such as
               'endpoints.devices.Devices.list_all'"""

    @wraps(fn)
    def wrapper_for_paginating(self, *args, **kwargs):
        """Performs the pagination."""
        if not self.dry_run:
            if not kwargs.get("params"):
                kwargs["params"] = {}

            has_more = True
            kwargs["params"].setdefault("limit", self.HTTP_PAGINATE_MAX_RESULTS)
            kwargs["params"].setdefault("starting_after", 0)

            while has_more:
                response = self.get(*args, **kwargs)
                json_data = response.json()
                objects = json_data.get("data", [])

                if objects:
                    for obj in objects:
                        yield obj

                    kwargs["params"]["starting_after"] = objects[-1].get("id")
                has_more = json_data.get("has_more", False)
        else:
            # do some action in dry run mode so something is returned
            self.get(*args, **kwargs)

    return wrapper_for_paginating


def url_suffixes(suffix: str, add_param_vals_to_url: Optional[list] = []):
    """Decorator for adding an additional suffix to the urls for certain SimpleMDM API methods that
    have additonal paths after a parameter like 'device_id'.
    Additionally, parameters from the 'endpoints' method can be subsequently added after the suffix.

    For example, by specifying 'bluetooth' as the 'suffix' value, the 'https://a.simplemdm.com/api/v1/devices/{id}'
    url will be modified to become 'https://a.simplemdm.com/api/v1/devices/{id}/bluetooth'.

    Items in the 'add_param_vals_to_url' are processed in order, and any matching param value is
    then added to the URL, for example, turning "@url_suffixes('custom_attribute_values', ['attr_name'])"
    into 'https://a.simplemdm.com/api/v1/devices/{id}/custom_attribute_values/{attr_name}''

    The 'new_path' value will be the default argument returned in 'fn(self, *args, **kwargs)' if there is no
    other existing parameter that would ordinarily be the consumed as the url path to join to the base url.
    For example, if there is no '{id}' for 'https://a.simplemdm.com/v1/devices/{id}' and 'bluetooth' is the
    suffix being added, then the url created will be 'https://a.simplemdm.com/v1/devices/bluetooth', this
    behaviour may change to raising a ValueError in a future update if this behaviour is troublesome.

    Note: This decorator should be applied as the last decorator of a method."""

    def wrapper_for_suffixing(fn: Callable) -> Callable:
        """Performs the suffix actions."""

        @wraps(fn)
        def wrap_action(self, *args, **kwargs) -> Callable:
            """This wraps the method and returns the function with a new set of *args"""
            params = kwargs.get("params", {})

            if params and add_param_vals_to_url:
                param_paths = [v for k, v in params.items() if k in add_param_vals_to_url]

                # remove the params from 'add_param_vals_to_url' as these are not passed as values in 'params'
                # because they'll form part of the url
                kwargs["params"] = {k: v for k, v in params.items() if k not in add_param_vals_to_url}
            else:
                param_paths = None

            try:
                new_path = f"{args[0]}/{suffix}"
            except IndexError:
                # fall back to just inserting the suffix; warning, this might not be the most appropriate path forward
                new_path = suffix
            finally:
                if param_paths:
                    param_paths = "/".join(param_paths)
                    new_path = f"{new_path}/{param_paths}"

                args = [new_path, *args[1:]] if args else [new_path]

            return fn(self, *args, **kwargs)

        return wrap_action

    return wrapper_for_suffixing
