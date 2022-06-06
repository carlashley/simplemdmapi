"""SimpleMDM API Connector.
class: SimpleMDMConnector
    parameters:
        token: token as a string, or a path to the file containing the token.
        base_url: base URL for the SimpleMDM API.
        timeout: a tuple of seconds for the connect timeout and read
                 timeout; default is 5 seconds for connection, and no
                 timeout for read.
        max_retry: number of times a request is retried before failing.
        retry_backoff: number of seconds between each retry, increases
                       exponentially based on this value.
        http_retry_statuses: list of HTTP status codes to retry on.

    methods:
        delete
        get
        paginate
        patch
        post
        put

    method parameters:
        url: partial URL path for any additional paths after the URL endpoint;
             example: 'devices/[device_id]' - this gets joined to the class
             'base_url' instance attribute, and the child class 'endpoint' instance
             attribute to form the full URL passed to the requests method, using the
             example url value, the full URL becomes:
                 https://a.simplemdm.com/api/v1/devices/[device_id]
        params: any additional parameters to pass on to the API;
                example: {"serial_number": "C012345QZS"}
        files: only used for API methods that upload files.
        ignore_statuses: do not raise exceptions for these HTTP status codes as the
                         API in some circumstances returns a status code that will
                         cause the requests 'raise_for_status' method to raise an
                         exception even though the status code indicates no actual
                         error has occurred (for example, the enable remote desktop
                         API method will return HTTP 400 if remote desktop is
                         already enabled)
        kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""

import requests

from .typehints import (ListInt,
                        OptionalDict,
                        OptionalListDict,
                        OptionalListString,
                        OptionalString,
                        TupleInt,
                        UnionStringPath)
from .validators import (parse_kwargs,
                         required_params,
                         validate_file_exts,
                         validate_params,
                         validate_unique_params)
from functools import wraps
from os import getenv
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry
from typing import Any

try:
    from .proxies import proxy_settings
except ImportError:
    proxy_settings = None
    pass

VALID_FILE_KEYS = ["binary", "file", "mobileconfig"]
VALID_FILE_EXTS = [".mobileconfig", ".pkg", ".plist", ".txt"]


def read_token(fp: UnionStringPath) -> str:
    """Read token from a file and return the token string, or return the string.
    :param fp: string or file path of token"""
    try:
        if Path(fp).is_file() and Path(fp).exists():
            with Path(fp).open("r") as f:
                return f.readlines()[0].strip()
        else:
            return fp
    except OSError as e:
        if e.errno == 63:  # Path too long, probably string!
            return fp


def urljoin(*args) -> str:
    """Join parts of a URL together to a full URL path."""
    return "/".join([x.strip("/") for x in args if x])


class APIException(Exception):
    """General API Exception"""
    pass


class APIParamException(APIException):
    """API Parameter exception"""
    pass


class APIUploadException(APIException):
    """API File Upload Exception"""
    pass


class SimpleMDMConnector:
    """Simple MDM API Connector
    :param token: token as a string, or a path to the file containing the token.
    :param base_url: base URL for the SimpleMDM API.
    :param timeout: a tuple of seconds for the connect timeout and read
                    timeout; default is 5 seconds for connection, and no
                    timeout for read.
    :param max_retry: number of times a request is retried before failing.
    :param retry_backoff: number of seconds between each retry, increases
                          exponentially based on this value.
    :param http_retry_statuses: list of HTTP status codes to retry on."""
    def __init__(self, token: UnionStringPath = getenv("SIMPLETOKEN"),
                 base_url: str = "https://a.simplemdm.com/api/v1",
                 timeout: TupleInt = (5, 15),
                 max_retry: int = 3,
                 retry_backoff: int = 1,
                 http_status_retries: ListInt = [429, 500, 502, 503, 504],) -> None:
        self._token = read_token(token)
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.proxies.update(proxy_settings) if proxy_settings else None
        self.session.mount("https://", HTTPAdapter(max_retries=Retry(total=max_retry,
                                                                     status_forcelist=http_status_retries,
                                                                     backoff_factor=retry_backoff)))
        self.session.auth = requests.auth.HTTPBasicAuth(self._token, '')

    def _prepare_request(self, method: str, url: str, params: OptionalDict = dict(),
                         files: OptionalDict = dict(), **kwargs) -> Any:
        """Create a prepared request for use with the session."""
        req = requests.Request(method=method, url=url, params=params, files=files)
        prepared_req = self.session.prepare_request(req)
        env_settings = self.session.merge_environment_settings(prepared_req.url, {}, None, None, None)

        return self.session.send(prepared_req, **env_settings, **kwargs)

    def _request(method: str):
        """Internal decorator method used for the requests package."""
        def decorator(func):
            @wraps(func)  # For docstring pass through from original function.
            def _inner(self, url: OptionalString = None,
                       params: OptionalDict = dict(), files: OptionalDict = dict(),
                       ignore_statuses: OptionalListString = list(), **kwargs):
                """Inner funciton that does the heavy lifing"""
                url = urljoin(self.base_url, self.endpoint, url)  # Join all URL paths together
                kwargs["timeout"] = kwargs.get("timeout", self.timeout)
                file_key = [k for k in VALID_FILE_KEYS if k in files] if files else None
                _required_params = kwargs.get("required_params", None)
                _validate_params = kwargs.get("validate_params", None)
                _unique_params = kwargs.get("unique_params", None)

                required_params(params, _required_params) if _required_params else None
                validate_params(params, _validate_params) if _validate_params else None
                validate_file_exts(files, VALID_FILE_KEYS) if files else None
                validate_unique_params(params, _unique_params) if _unique_params else None
                parse_kwargs(kwargs)  # Pull any kwargs out that should not be passed to 'requests'

                # Completely ensure no files are passed to a REST action that does not accept
                # file upload.
                if method in ["GET", "DELETE", "PATH"] and files:
                    files = dict()

                # Use context based file handling
                if files and file_key:
                    try:
                        fp = files.copy()[file_key][0]  # Work on a copy of the dict for safety
                        self.validate_file_extensions(fp, VALID_FILE_EXTS)

                        with open(fp, "rb") as f:
                            files[file_key[0]] = f
                            req = self._prepare_request(method=method, url=url, params=params, files=files, **kwargs)
                    except KeyError:
                        raise
                else:
                    req = self._prepare_request(method=method, url=url, params=params, files=files, **kwargs)

                # Only raies HTTP status exceptions
                req.raise_for_status() if req.status_code not in ignore_statuses else None
                return req
            return _inner
        return decorator

    @_request("DELETE")
    def delete(self, url: OptionalString = None, params: OptionalDict = dict(),
               files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Delete"""
        return url, params, files, kwargs

    @_request("GET")
    def get(self, url: OptionalString = None, params: OptionalDict = dict(),
            files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Get"""
        return url, params, files, kwargs

    @_request("PATCH")
    def patch(self, url: OptionalString = None, params: OptionalDict = dict(),
              files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Patch"""
        return url, params, files, kwargs

    @_request("POST")
    def post(self, url: OptionalString = None, params: OptionalDict = dict(),
             files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Post"""
        return url, params, files, kwargs

    @_request("PUT")
    def put(self, url: OptionalString = None, params: OptionalDict = dict(),
            files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Put"""
        return url, params, files, kwargs

    def paginate(self, url: OptionalString = None, params: OptionalDict = dict(),
                 has_more: bool = True, limit: int = 100, starting_after: int = 0,
                 ignore_statuses: OptionalListString = list(), **kwargs) -> OptionalListDict:
        """Paginate"""
        result: OptionalListDict = list()
        paginate_params = ["limit", "starting_after"]  # Required for pagination

        if not kwargs.get("validate_params"):
            kwargs["validate_params"] = paginate_params
        else:
            kwargs["validate_params"].extend(paginate_params)

        if not params:
            params["limit"] = limit
            params["starting_after"] = starting_after

        while has_more:
            req = self.get(url=url, params=params, files=dict(), ignore_statuses=ignore_statuses, **kwargs)

            if has_more and req.json() and req.json().get("data"):
                result.extend(req.json()["data"])
                params["starting_after"] = str(req.json()["data"][-1].get("id"))
                has_more = req.json().get("has_more", False)
            else:
                if req.json().get("data"):
                    result.extend(req.json()["data"])
                    has_more = req.json().get("has_more", False)
                else:
                    break

        return result
