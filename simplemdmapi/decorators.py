from functools import wraps
from pathlib import Path
from requests.models import Response
from time import sleep
from typing import Callable, Optional
from .utils import api_error_check, consume_func_kwargs, consume_kwargs, generate_url, session_retry
from .validators import validate_any, validate_incompatible, validate_package, validate_param_opts, validate_required


# def _wait(s: int | float) -> None:
#     """Perform a wait between each request.
#     :param s: time value in seconds"""
#     if s > 0:
#         sleep(s)


def method_params(fn: Callable) -> Callable:
    """Decorator for performing validations and other actions on an API method.
    Note: This decorator must be first in the decorator chain."""

    @wraps(fn)
    def wrap_actions(self, *args, **kwargs) -> Callable:
        fn_name = fn.__name__
        conf = self._method_kwargs.get(fn_name, {})

        any_params = conf.get("any_params")
        req_params = conf.get("req_params")
        inc_params = conf.get("inc_params")
        val_params = conf.get("validate")
        file_param = conf.get("file_param")
        file = kwargs.get(file_param)

        if req_params:
            validate_required(kwargs, req_params, fn_name)

        if any_params:
            validate_any(kwargs, any_params, fn_name)

        if inc_params:
            validate_incompatible(kwargs, inc_params, fn_name)

        if val_params:
            validate_param_opts(kwargs, val_params, fn_name)

        if file and file_param == "binary":
            _file = Path(file)

            if _file.suffix == ".pkg":
                validate_package(_file, fn_name)

        # do a switcharoo on kwargs if there is a "file"
        if not kwargs.get("files") and file:
            kwargs["files"] = {file_param: file}
            kwargs["file_upload"] = file_param  # need this for request post
            del kwargs[file_param]  # not required, so discard

        return fn(self, *args, **kwargs)

    return wrap_actions


def paginate(fn: Callable) -> Callable:
    """Perform pagination action on endpoint methods that require it.
    Note: This decorator must be placed after the 'method_params' and 'url_suffixes' decorators if an API method is
          decorated with 'method_params' and/or 'url_suffixes'.

    Parameters that can be included in the kwargs of the decorated function that relate to pagination:
    :param limit: optional limit on the number of objects returned per 'page'; default is 100
    :param starting_after: optional cursor in the form of an object id, typically this is the last object id
                           in the response, if unspecified, the API starts at the beginning of the object list
    :param direction: optional string indicating sort direction, values are either 'asc' or 'desc',
                      default is 'asc'"""

    @wraps(fn)
    def wrap_actions(self, *args, **kwargs) -> Callable:
        paginate = True
        limit = kwargs.get("limit", 100)
        starting_after = kwargs.get("starting_after", 0)
        direction = kwargs.get("direction", "asc")
        kwargs.setdefault("limit", limit)
        kwargs.setdefault("starting_after", starting_after)
        kwargs.setdefault("direction", direction)

        if not self.dry_run:
            while paginate:
                # _wait(self.HTTP_SLEEP_WAIT)
                response = self.get(*args, **kwargs)
                json_data = response.json()
                objects = json_data.get("data", [])

                if objects:
                    kwargs["starting_after"] = objects[-1].get("id")
                    paginate = json_data.get("has_more", False)

                    for obj in objects:
                        yield obj
                else:
                    paginate = False
        else:
            self.get(*args, **kwargs)

    return wrap_actions


def request(method: str) -> Callable:
    """Decorator for wrapping REST methods.
    :param method: string, REST method to perform; 'delete', 'get', 'patch', 'post', or 'put'
                   are all valid values."""
    methods = ["delete", "get", "patch", "post", "put"]

    if method not in methods:
        raise ValueError(f"Error: {method!r} is an invalid REST method; use one of: {methods}")

    method = method.upper()

    def wrap_function(fn: Callable) -> Callable:
        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Response:
            rqst_kwargs, func_kwargs = consume_kwargs(**kwargs)
            ignore, retry = consume_func_kwargs(self, **func_kwargs)
            fieldname = func_kwargs.get("file_upload")
            url = generate_url(self, *args)

            # gotta let uploads take the time they need
            if not fieldname and not rqst_kwargs.get("files"):
                rqst_kwargs.setdefault("timeout", (self.HTTP_CONNECT_TIMEOUT, self.HTTP_READ_TIMEOUT))

            if rqst_kwargs.get("json"):
                rqst_kwargs["headers"] = {"Content-Type": "application/json"}

            self.session.mount("https://", session_retry(self, retry))

            if not self.dry_run:
                # _wait(self.HTTP_SLEEP_WAIT)

                if fieldname and rqst_kwargs.get("files"):
                    file = Path(rqst_kwargs["files"].get(fieldname)).expanduser().resolve()

                    with file.open("rb") as f:
                        rqst_kwargs["files"][fieldname] = f
                        response = self.session.request(method, url, **rqst_kwargs)

                        if response.status_code not in ignore:
                            response.raise_for_status()

                        return response
                else:
                    response = self.session.request(method, url, **rqst_kwargs)

                    if response.status_code not in ignore or response.status_code not in self.HTTP_RETRY_STATUS_LIST:
                        api_error_check(response)  # this should catch API specific error responses
                        response.raise_for_status()  # this should catch HTTP connection exceptions that are missed

                    return response
            else:
                print(f"Perform {method!r} on {url!r} with kwargs {rqst_kwargs}")

        return wrap_actions

    return wrap_function


def url_suffixes(sfx: str, params_as_suffixes: Optional[list] = []) -> Callable:
    """Decorator for adding a suffix string and parameter values as suffixes to a URL.
    For example: decorating 'device_groups.assign_device' with @url_suffixes("devices", ["device_id"]) will result in
    a URL like so:
        https://a.simplemdm.com/api/v1/device_groups/{group_id}/devices/{device_id}

    Note: This decorator must be placed before the 'paginate' decorator, and after the 'method_params' decorator."""

    def wrap_function(fn: Callable) -> Callable:
        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Callable:
            paths = "/".join([sfx, *[v for k, v in kwargs.items() if k in params_as_suffixes]])

            # update args and kwargs, note, any kwarg key that exists in 'params_as_suffixes' is discarded,
            # those values are not supposed to be passed in as params as they form the URL being acted on.
            args = [*args, paths] if args else [paths]
            kwargs = {k: v for k, v in kwargs.copy().items() if k not in params_as_suffixes}

            return fn(self, *args, **kwargs)

        return wrap_actions

    return wrap_function
