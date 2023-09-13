from functools import wraps
from itertools import combinations
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response
from typing import Callable, Optional

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


def _consume_request_kwargs(**kwargs) -> tuple[dict, dict]:
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


def method_params(fn) -> Callable:
    """Decorator for parsing the endpoint method parameters into a 'params' keyword argument dictionary
    object that is then parsed back in a cleaned up kwargs object.
    :param fn: the function that is being decorated"""

    @wraps(fn)
    def wrap_actions(self, *args, **kwargs) -> Callable:
        """Wrapper to perform actions on the wrapped fucntion from 'wrap_function'."""
        _class = self.__class__.__name__
        _fnctn = fn.__name__
        param_conf = self._method_kwargs.get(_class, {}).get(_fnctn, {})
        all_params = param_conf.get("all_params", [])
        any_params = param_conf.get("any_params", [])
        req_params = param_conf.get("req_params", [])
        inc_params = param_conf.get("inc_params", [])
        val_params = param_conf.get("validate", {})
        file_param = param_conf.get("file_param")
        bad_combos = _generate_bad_combinations(inc_params)

        # Check all required method parameters are provided
        if req_params:
            for req_param in req_params:
                if req_param not in kwargs:
                    raise TypeError(f"{_fnctn}() missing required keyword-only parameter: {req_param!r}")

        # Check any optional parameters where at least one optional parameter is required
        if any_params:
            if not any(any_param in kwargs for any_param in any_params):
                raise TypeError(f"{_fnctn}() missing at least one optional keyword-only parameter: {any_params}")

        # Check any incompatible parameter combinations
        if inc_params:
            for kwarg in kwargs:
                for combo in bad_combos:
                    for bad_kwarg in combo:
                        if bad_kwarg in kwargs and kwarg in inc_params and not bad_kwarg == kwarg:
                            raise AttributeError(f"{_fnctn}() {bad_kwarg!r} not permitted with {kwarg!r}")

        # Validate any parameter values
        if val_params:
            for param, values in val_params.items():
                value = kwargs.get(param)

                if value and value not in values:
                    err = f"{_fnctn}() unexpected value {value!r} for {param!r}, expecting one of: {values}"
                    raise ValueError(err)

        files = {file_param: kwargs.get(file_param)}
        request_params = {
            k: v for k, v in kwargs.copy().items() if k in all_params and file_param and not k == file_param
        }
        request_params["files"] = files
        kwargs = {k: v for k, v in kwargs.copy().items() if k not in all_params}
        kwargs["params"] = request_params

        return fn(self, *args, **kwargs)

    return wrap_actions


# def param_kwargs(params: list[str]) -> Callable:
#     """Decorator for internal methods that have parameters to be passed as params to the underlying request.
#     :param params: list of strings representing the kwarg keys that are params."""
#
#     def wrap_function(fn: Callable) -> Callable:
#         """Wraps the method that has the params to parse.
#         :param fn: the callable being decorated"""
#
#         @wraps(fn)
#         def wrap_actions(self, *args, **kwargs) -> Callable:
#             """Wrapper to perform actions on the wrapped fucntion from 'wrap_function'."""
#             print(f"param_kwargs decorator: pre: {kwargs}")
#             rqst_params, kwargs = _consume_param_kwargs(params, **kwargs)
#             kwargs["params"] = rqst_params
#             print(f"param_kwargs decorator: post: {kwargs}")
#
#             # raise type error for unexpected kwargs
#             for k, _ in kwargs.items():
#                 if k not in [*params, *_requests_kwargs, "ignore_statuses", "retry_statuses"]:
#                     raise TypeError(f"{fn.__name__}() got an unexpected keyword argument {k!r}")
#
#             return fn(self, *args, **kwargs)
#
#         return wrap_actions
#
#     return wrap_function


def file_upload(fn: Callable) -> Callable:
    """Decorator for internal methods that have a file upload to process.
    :param fn: the function that is being decorated"""

    @wraps(fn)
    def wrap_actions(self, *args, **kwargs) -> Response:
        """Wrapper to perform actions on the wrapped function from 'wrap_function'"""
        # note, some API methods have an option to upload a file, depending on the parameters
        # passed, for example, the apps.create method can optionally upload a file to SimpleMDM,
        # so test for the existence of an upload file fieldname, and return a post response
        # either way
        _class = self.__class__.__name__
        _fnctn = fn.__name__
        param_conf = self._method_kwargs.get(_class, {}).get(_fnctn, {})
        file_fn = param_conf.get("file_param")
        print(f"file_upload pre processing args, kwargs: {args}, {kwargs}")

        if file_fn in kwargs.get("params", {}):
            filename = kwargs["params"].get(file_fn)

            del kwargs["params"][file_fn]  # not needed in params anymore

            with open(filename, "rb") as f:
                kwargs["files"] = {file_fn: f}
                response = self.post(*args, **kwargs)
                return response
        else:
            return self.post(*args, **kwargs)

    return wrap_actions


def request(method: str) -> Callable:
    """Decorator for internal methods that require a requests.Session method call.
    :param method: the REST method action to perform, for example 'delete', 'get', 'patch', 'post', 'put'"""

    def wrap_function(fn: Callable) -> Callable:
        """This wraps the method performing the REST action; for example self.get(url) is decorated with '@request',
        so the self.get() method is being wrapped."""

        @wraps(fn)  # keep docstrings, and arguments from original function
        def wrap_actions(self, *args, **kwargs) -> Response:
            """Wrapper to perform actions on the wrapped function from 'wrap_function'."""
            print(f"request dry_run: {self.dry_run}")
            print(f"request kwargs (start): {kwargs}")
            # pre-process arguments, consuming args and kwargs
            print(f"request {kwargs}")
            rqst_kwargs, func_kwargs = _consume_request_kwargs(**kwargs)
            ignore, retry = _consume_status_kwargs(self, **func_kwargs)
            print(f"consumed rqst_kwargs: {rqst_kwargs}, func_kwargs, {func_kwargs}")

            if args:
                url_path, rqst_args = _consume_url(*args)
            else:
                url_path, rqst_args = None, []

            url = urljoin(self.api_vers, self.endpoint, url_path, base_url=self.BASE_URL)
            print(f"urljoined: {url}, rqst_args: {rqst_args}")

            # modify the session with some values
            rqst_kwargs.setdefault("timeout", (self.HTTP_CONNECT_TIMEOUT, self.HTTP_READ_TIMEOUT))
            self.session.mount(
                "https://",
                HTTPAdapter(
                    max_retries=Retry(
                        total=self.HTTP_MAX_RETRIES, status_forcelist=retry, backoff_factor=self.HTTP_RETRY_BACKOFF
                    )
                ),
            )

            if self.dry_run and not method.lower() == "get":
                print(f"perform {method!r} on {url!r} with args {rqst_args} and kwargs {rqst_kwargs}")
            else:
                return None
            # # now perform the request
            # response = self.session.request(method, url, *rqst_args, **rqst_kwargs)

            # # handle any exceptions that should raise a HTTP status exception, except when it's
            # # ok to safely ignore those errors
            # if response.status_code not in ignore:
            #     response.raise_for_status()

            # return response  # return the object

        return wrap_actions

    return wrap_function


def paginate(fn: Callable) -> Callable:
    """Decorator for API methods that require paginating a response from a 'get' request.
    :param fn: callable"""

    @wraps(fn)
    def wrapper_for_paginating(self, *args, **kwargs):
        """Performs the pagination."""
        print(f"paginate args, kwargs: {args}, {kwargs}")
        has_more = True
        existing_params = kwargs.get("params", {})
        kwargs, params = _consume_request_kwargs(**kwargs)  # don't use consume_param_kwargs, keep actual params intact
        params.setdefault("limit", 100)
        params.setdefault("starting_after", 0)
        params.update(existing_params)
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
    Note: This decorator should be applied as the last decorator of a method.
    Items in the 'add_kwargs_vals_to_url' are processed in order, and any matching kwarg value is
    then added to the URL, for example, turning url_suffixes('custom_attribute_values', ["attr_name"])
    into:
        https://a.simplemdm.com/api/v1/devices/{id}/custom_attribute_values/{attr_name}"""

    def wrapper_for_suffixing(fn: Callable) -> Callable:
        """Performs the suffix actions."""

        @wraps(fn)
        def wrap_action(self, *args, **kwargs) -> Callable:
            """This wraps the method and returns the function with a new set of *args"""
            print(fn.__name__)
            # a list of values from kwargs["params"] that need to get added to the URL
            if kwargs.get("params"):
                url_kwarg_param_vals = [v for k, v in kwargs["params"].items() if k in add_kwarg_vals_to_url]
                # update params to reflect consumed values that don't get posted as a param because they form
                # part of the url
                kwargs["params"] = {k: v for k, v in kwargs["params"].items() if k not in add_kwarg_vals_to_url}
            else:
                url_kwarg_param_vals = []

            try:
                new_path = f"{args[0]}/{suffix}"
            except IndexError:
                # this may have unintended consequences as it is untested if this is the appropriate action to take
                raise Exception(f"Error: could not append {suffix!r} to URL")
            finally:
                if add_kwarg_vals_to_url:
                    values_path = "/".join(kwargs.get(v) for v in url_kwarg_param_vals)
                    new_path = f"{new_path}/{values_path}"

                args = [new_path, *args[1:]] if args else [new_path]
                print(f"url_suffixes args, kwargs: {args}, {kwargs}")
                return fn(self, *args, **kwargs)

        return wrap_action

    return wrapper_for_suffixing
