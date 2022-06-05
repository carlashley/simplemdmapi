import requests

from .typehints import (ListInt,
                        ListString,
                        ListTupleString,
                        OptionalDict,
                        OptionalListDict,
                        OptionalListString,
                        OptionalString,
                        RequiredDict,
                        TupleInt,
                        UnionStringPath)
from functools import wraps
from itertools import combinations
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry


def parse_kwargs(kwargs: RequiredDict) -> RequiredDict:
    """Pre-parse kwarg dictionary to remove keys that are parameters
    interhited from class properties or elsewhere."""
    del_kwargs = ["required_params",
                  "url",
                  "unique_params",
                  "validate_params"]

    for k, in del_kwargs:
        try:
            del kwargs[k]
        except KeyError:
            pass

    return kwargs


def read_token(fp: UnionStringPath) -> str:
    """Read token from a file and return the token string, or
    return the string.
    :param fp: string or file path of token"""
    if not isinstance(fp, Path):
        fp = Path(fp)

    if fp.is_file() and fp.exists():
        with fp.open("r") as f:
            return f.readlines()[0].strip()
    else:
        return str(fp)


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
    def __init__(self, token: UnionStringPath,
                 base_url: str = "https://a.simplemdm.com/api/v1",
                 timeout: TupleInt = (5, ),
                 max_retry: int = 3,
                 retry_backoff: int = 1,
                 http_status_retries: ListInt = [429, 500, 502, 503, 504],) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=Retry(total=max_retry,
                                                                     status_forcelist=http_status_retries,
                                                                     backoff_factor=retry_backoff)))
        self.session.auth = requests.auth.HTTPBasicAuth(read_token(token), '')

    def required_params(self, params: RequiredDict, reqrd_params: ListString) -> None:
        """Required parameters.
        :param params: dictionary of API parameters to validate.
        :param reqrd_params: list of required paramater names that are required."""
        msg_params: ListString = list()
        msg_params = [param for param in params if param not in reqrd_params]

        if msg_params:
            raise APIParamException(f"Invalid parameters: {msg_params}; required parameters: {reqrd_params}")

    def unique_params(self, params: RequiredDict, unique_params: ListString) -> None:
        """Unique parameters.
        :param params: dictionary of API parameters to validate.
        :param unique_params: list of paramater names that must be unique."""
        permutations: ListTupleString = list()

        for num in range(1, len(unique_params) + 1):
            permutations.extend(list(combinations(unique_params, num)))

        if tuple(params) in permutations:
            raise APIParamException(f"Error: Only unique combinations can be supplied, use one of: {unique_params}")

    def validate_file_extensions(self, fp: UnionStringPath, valid_exts: ListString) -> None:
        """Validate file extensions before upload.
        :param files: list of file paths as a string, or file paths
        :param valid_exts: list of valid file extensions."""
        if Path(fp).suffix not in valid_exts:
            raise APIUploadException(f"Invalid file extension for file {str(fp)!r}; valid extensions: {valid_exts}")

    def validate_params(self, params: RequiredDict, valid_params: ListString) -> None:
        """Validate parameters.
        :param params: dictionary of API parameters to validate.
        :param valid_params: list of required paramater names to validate against."""
        msg_params: ListString = list()
        msg_params = [param for param in params if param not in valid_params]

        if msg_params:
            raise APIParamException(f"Invalid parameters: {msg_params}; valid parameters: {valid_params}")

    def _request(method: str):
        """Internal decorator method used for the requests package."""
        def decorator(func):
            @wraps(func)  # For docstring pass through from original function.
            def _inner(self, url: OptionalString = None,
                       params: OptionalDict = dict(), files: OptionalDict = dict(),
                       ignore_statuses: OptionalListString = list(), **kwargs):
                """Perform the specified 'requests.request' method.
                :param url: partial URL path for any additional paths after the URL endpoint;
                            example: 'devices/[device_id]' - this gets joined to the class
                            'base_url' instance attribute, and the child class 'endpoint' instance
                            attribute to form the full URL passed to the requests method, using the
                            example url value, the full URL becomes:
                                https://a.simplemdm.com/api/v1/devices/[device_id]
                :param params: any additional parameters to pass on to the API;
                               example: {"serial_number": "C012345QZS"}
                :param files: any files to upload to the API;
                              example: {"binary": "/tmp/simplemdmapi.pkg"}
                :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                        API in some circumstances returns a status code that will
                                        cause the requests 'raise_for_status' method to raise an
                                        exception even though the status code indicates no actual
                                        error has occurred (for example, the enable remote desktop
                                        API method will return HTTP 400 if remote desktop is
                                        already enabled)
                :param kwargs: any additional arguments to provide to the underlying requests call;
                               example: {"timeout": (5, 15)}"""
                kwargs["timeout"] = kwargs.get("timeout", self.timeout)
                valid_file_keys = ["binary", "file", "mobileconfig"]
                valid_file_exts = [".mobileconfig", ".pkg", ".plist", ".txt"]
                file_key = [k for k in valid_file_keys if k in files] if files else None
                required_params = kwargs.get("required_params", None)
                validate_params = kwargs.get("validate_params", None)
                unique_params = kwargs.get("unique_params", None)
                self.required_params(params, required_params) if required_params else None
                self.validate_params(params, validate_params) if validate_params else None
                self.validate_params(files, valid_file_keys) if files else None
                self.unique_params(params, unique_params) if unique_params else None
                parse_kwargs(kwargs)  # Pull any kwargs out that should not be passed to 'requests'
                url = urljoin(self.base_url, self.endpoint, url)  # Join all URL paths together

                # Completely ensure no files are passed to a REST action that does not accept
                # file upload.
                if method in ["GET", "DELETE", "PATH"] and files:
                    files = dict()

                # Use context based file handling
                if files and file_key:
                    try:
                        fp = files.copy()[file_key][0]  # Work on a copy of the dict for safety
                        self.validate_file_extensions(fp, valid_file_exts)

                        with open(fp, "rb") as f:
                            files[file_key[0]] = f
                            req = requests.request(method=method, url=url, params=params, files=files, **kwargs)
                    except KeyError:
                        raise
                else:
                    req = requests.request(method=method, url=url, params=params, files=files, **kwargs)

                # Only raies HTTP status exceptions
                req.raise_for_status() if req.status_code not in ignore_statuses else None
                return req
            return _inner
        return decorator

    @_request("DELETE")
    def delete(self, url: OptionalString = None, params: OptionalDict = dict(),
               files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Perform the specified 'requests.request' method.
        :param url: partial URL path for any additional paths after the URL endpoint;
                    example: 'devices/[device_id]' - this gets joined to the class
                    'base_url' instance attribute, and the child class 'endpoint' instance
                    attribute to form the full URL passed to the requests method, using the
                    example url value, the full URL becomes:
                        https://a.simplemdm.com/api/v1/devices/[device_id]
        :param params: any additional parameters to pass on to the API;
                       example: {"serial_number": "C012345QZS"}
        :param files: unused
        :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                API in some circumstances returns a status code that will
                                cause the requests 'raise_for_status' method to raise an
                                exception even though the status code indicates no actual
                                error has occurred (for example, the enable remote desktop
                                API method will return HTTP 400 if remote desktop is
                                already enabled)
        :param kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""
        return url, params, files, kwargs

    @_request("GET")
    def get(self, url: OptionalString = None, params: OptionalDict = dict(),
            files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Perform the specified 'requests.request' method.
        :param url: partial URL path for any additional paths after the URL endpoint;
                    example: 'devices/[device_id]' - this gets joined to the class
                    'base_url' instance attribute, and the child class 'endpoint' instance
                    attribute to form the full URL passed to the requests method, using the
                    example url value, the full URL becomes:
                        https://a.simplemdm.com/api/v1/devices/[device_id]
        :param params: any additional parameters to pass on to the API;
                       example: {"serial_number": "C012345QZS"}
        :param files: unused
        :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                API in some circumstances returns a status code that will
                                cause the requests 'raise_for_status' method to raise an
                                exception even though the status code indicates no actual
                                error has occurred (for example, the enable remote desktop
                                API method will return HTTP 400 if remote desktop is
                                already enabled)
        :param kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""
        return url, params, files, kwargs

    @_request("PATCH")
    def patch(self, url: OptionalString = None, params: OptionalDict = dict(),
              files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Perform the specified 'requests.request' method.
        :param url: partial URL path for any additional paths after the URL endpoint;
                    example: 'devices/[device_id]' - this gets joined to the class
                    'base_url' instance attribute, and the child class 'endpoint' instance
                    attribute to form the full URL passed to the requests method, using the
                    example url value, the full URL becomes:
                        https://a.simplemdm.com/api/v1/devices/[device_id]
        :param params: any additional parameters to pass on to the API;
                       example: {"serial_number": "C012345QZS"}
        :param files: unused
        :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                API in some circumstances returns a status code that will
                                cause the requests 'raise_for_status' method to raise an
                                exception even though the status code indicates no actual
                                error has occurred (for example, the enable remote desktop
                                API method will return HTTP 400 if remote desktop is
                                already enabled)
        :param kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""
        return url, params, files, kwargs

    @_request("POST")
    def post(self, url: OptionalString = None, params: OptionalDict = dict(),
             files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Perform the specified 'requests.request' method.
        :param url: partial URL path for any additional paths after the URL endpoint;
                    example: 'devices/[device_id]' - this gets joined to the class
                    'base_url' instance attribute, and the child class 'endpoint' instance
                    attribute to form the full URL passed to the requests method, using the
                    example url value, the full URL becomes:
                        https://a.simplemdm.com/api/v1/devices/[device_id]
        :param params: any additional parameters to pass on to the API;
                       example: {"serial_number": "C012345QZS"}
        :param files: any files to upload to the API;
                      example: {"binary": "/tmp/simplemdmapi.pkg"}
        :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                API in some circumstances returns a status code that will
                                cause the requests 'raise_for_status' method to raise an
                                exception even though the status code indicates no actual
                                error has occurred (for example, the enable remote desktop
                                API method will return HTTP 400 if remote desktop is
                                already enabled)
        :param kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""
        return url, params, files, kwargs

    @_request("PUT")
    def put(self, url: OptionalString = None, params: OptionalDict = dict(),
            files: OptionalDict = dict(), ignore_statuses: OptionalListString = list(), **kwargs):
        """Perform the specified 'requests.request' method.
        :param url: partial URL path for any additional paths after the URL endpoint;
                    example: 'devices/[device_id]' - this gets joined to the class
                    'base_url' instance attribute, and the child class 'endpoint' instance
                    attribute to form the full URL passed to the requests method, using the
                    example url value, the full URL becomes:
                        https://a.simplemdm.com/api/v1/devices/[device_id]
        :param params: any additional parameters to pass on to the API;
                       example: {"serial_number": "C012345QZS"}
        :param files: any files to upload to the API;
                      example: {"binary": "/tmp/simplemdmapi.pkg"}
        :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                API in some circumstances returns a status code that will
                                cause the requests 'raise_for_status' method to raise an
                                exception even though the status code indicates no actual
                                error has occurred (for example, the enable remote desktop
                                API method will return HTTP 400 if remote desktop is
                                already enabled)
        :param kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""
        return url, params, files, kwargs

    def paginate(self, url: OptionalString = None, params: OptionalDict = dict(),
                 has_more: bool = True, limit: int = 100, starting_after: int = 0,
                 ignore_statuses: OptionalListString = list(), **kwargs) -> OptionalListDict:
        """Paginate function for iterating over endpoints that require pagination.
        :param url: partial URL path for any additional paths after the URL endpoint;
                     example: devices/[device_id]
        :param params: any additional parameters to pass on to the API;
                       example: {"serial_number": "C012345QZS"}
        :param limit: maximum number of objects the API will return for each page iteration
        :param starting_after: the 'offset' value for the next iteration of pagination to start from,
                               this is usually the 'id' value of the last object returned in the response
        :param ignore_statuses: do not raise exceptions for these HTTP status codes as the
                                API in some circumstances returns a status code that will
                                cause the requests 'raise_for_status' method to raise an
                                exception even though the status code indicates no actual
                                error has occurred (for example, the enable remote desktop
                                API method will return HTTP 400 if remote desktop is
                                already enabled)
        :param kwargs: any additional arguments to provide to the underlying requests call;
                       example: {"timeout": (5, 15)}"""
        result: OptionalListDict = list()

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
