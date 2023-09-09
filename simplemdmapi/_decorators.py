from functools import wraps
from typing import Any, Callable, Optional

from ._utilities import urljoin


def file_upload(form_field: str, param_keys: list[str]):
    """Decorator for performing a file upload for a given API endpoint.
    :param form_filed: the name of the field in the form that the file is uploaded to; valid values
                       are 'binary', 'file', 'mobileconfig'
    :param param_keys: list of parameter names that can be provided to the paginated method"""
    valid_fields = ["binary", "file", "mobileconfig"]

    if form_field not in valid_fields:
        raise ValueError(f"Error: invalid value for 'form_field'; valid values are: {valid_fields}")

    def wrapper_a(fn: Callable):
        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            """Wrapper that is wrapped around the callable object that has been decorated.
            :params *args: positional arguments that are paramters of the decorated function
            :params **kwargs: positional keyword arguments that are parameters of the decorated
                              function"""
            file = kwargs.get(form_field)
            kwargs.setdefault("params", {k: v for k, v in kwargs.items() if k in param_keys})

            for k in param_keys:
                try:
                    del kwargs[k]
                except KeyError:
                    pass

            if file:
                with open(file, "rb") as f:
                    kwargs.setdefault("files", {form_field: f})

                    try:
                        del kwargs[form_field]
                    except KeyError:
                        pass
                    return self.post(*args, **kwargs)

        return wrapper_b

    return wrapper_a


def request(method: str) -> Any:
    """Decorator for performing the specified REST method.
    :param method: string representation of the REST method to perform; valid values are:
                   - 'delete'/'DELETE'
                   - 'get'/'GET'
                   - 'patch'/'PATCH'
                   - 'post'/'POST'
                   - 'put'/'PUT'"""

    def wrapper_a(fn: Callable):
        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            """Wrapper that is wrapped around the callable object that has been decorated.
            :params *args: positional arguments that are paramters of the decorated function
            :params **kwargs: positional keyword arguments that are parameters of the decorated
                              function"""
            url = urljoin(self.BASE_URL, self.endpoint, args[0] if args and len(args) > 0 else None)
            req_args = args[1:]
            req_kwargs, fn_kwargs = self._parse_kwargs(kwargs)
            req_kwargs.setdefault("timeout", (self.HTTP_CONNECT_TIMEOUT, self.HTTP_READ_TIMEOUT))
            ignore_status_errs = self._ignore_status_errs(fn_kwargs.get("ignore_status_errs", []))
            retry_status_codes = self._retry_status_codes(fn_kwargs.get("retry_status_codes", []))

            self.session.mount("https://", self._session_retry(retry_status_codes))
            response = self.session.request(method, url, *req_args, **req_kwargs)

            if response.status_code not in ignore_status_errs:
                response.raise_for_status()
            return response

        return wrapper_b

    return wrapper_a


def paginate(fn: Callable):
    """Decorator for performing pagination over an API endpoint where pagination is required.
    :param fn: the method that is being decorated"""

    @wraps(fn)
    def wrapper_a(self, *args, **kwargs):
        """Wrapper that is wrapped around the callable object that has been decorated.
        :params *args: positional arguments that are paramters of the decorated function
        :params **kwargs: positional keyword arguments that are parameters of the decorated
                          function"""
        has_more = True

        while has_more:
            response = self.get(*args, **kwargs)
            json_data = response.json()
            objects = json_data.get("data", [])

            if objects:
                for obj in objects:
                    yield obj

                kwargs["params"]["starting_after"] = objects[-1].get("id")
            has_more = json_data.get("has_more", False)

    return wrapper_a


def api_path_suffix(suffix: str, kwargs_to_url: Optional[list] = []):
    """Decorator for adding a suffix to a URL, for example, adding "/bluetooth" to a device id.
    Optionally provide a list of kwargs to append to the URL _after_ the suffix
    :param suffix: string value to add to the end of a URL value (this is the first indice in *args)
    :param kwargs_to_url: a list of kwargs  to add after the suffix, joined by '/'"""

    def wrapper_a(fn: Callable):
        """Wrapper that is wrapped around the callable object that has been decorated.
        :params *args: positional arguments that are paramters of the decorated function
        :params **kwargs: positional keyword arguments that are parameters of the decorated
                          function"""

        @wraps(fn)
        def wrapper_b(self, *args, **kwargs):
            try:
                url = f"{args[0]}/{suffix}"
            except IndexError:
                url = suffix  # falls back to inserting the suffix as the URL value

            if kwargs_to_url:
                opt_k_url = "/".join(kwargs.get(ok) for ok in kwargs_to_url)
                url = f"{url}/{opt_k_url}"

                for k in kwargs.copy():
                    if k in kwargs_to_url:
                        try:
                            del kwargs[k]
                        except KeyError:
                            pass

            _args = [url, *args[1:]] if args else [url]
            return fn(self, *_args, **kwargs)

        return wrapper_b

    return wrapper_a
