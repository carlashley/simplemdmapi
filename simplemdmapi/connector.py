"""SimpleMDM API Connector."""
import inspect
import requests

from .typehints import (Function,
                        ListInt,
                        ListString,
                        OptionalDict,
                        OptionalString,
                        RequiredDict,
                        RequestsResponse,
                        TupleAny,
                        TupleInt,
                        UnionStringPath)
from .validators import VALID_FILE_KEYS
from os import getenv
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry

try:
    from .proxies import proxy_settings
except ImportError:
    proxy_settings = None
    pass


def clean_kwargs(kwargs: RequiredDict) -> RequiredDict:
    """Clean the kwarg dictionary to remove keys that are not standard 'requests.request' API params."""
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
    """Return a URL joined together."""
    return "/".join([x.strip("/") for x in args if x])


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

    def _parser(self, url: OptionalString = None, **kwargs) -> TupleAny:
        """Pre parse all internal HTTP request methods."""
        url = urljoin(self.base_url, self.endpoint, url)
        ignore_statuses = kwargs.get("ignore_statuses", list())
        kwargs = clean_kwargs(kwargs)
        kwargs["timeout"] = kwargs.get("timeout", self.timeout)

        return url, ignore_statuses, kwargs

    def delete(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """DELETE"""
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = self.session.delete(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def get(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """GET"""
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = self.session.get(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def patch(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """PATCH"""
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = self.session.patch(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def post(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """POST"""
        upload_key = kwargs.get("upload_key")
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = None

        if kwargs.get("files"):
            fp = Path(kwargs["files"][upload_key])

            with fp.open("rb") as f:
                kwargs["files"][upload_key] = f
                req = self.session.post(url, **kwargs)
        else:
            req = self.session.post(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def put(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """PUT"""
        upload_key = kwargs.get("upload_key")
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = None

        if kwargs.get("files"):
            fp = Path(kwargs["files"][upload_key])

            with fp.open("rb") as f:
                kwargs["files"][upload_key] = f
                req = self.session.put(url, **kwargs)
        else:
            req = self.session.put(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def paginate(self, url: OptionalString = None, starting_after: int = 0, limit: int = 100,
                 has_more: bool = True, **kwargs) -> RequiredDict:
        """Paginate over results.
        :param url: URL to paginate
        :param starting_after: record to start indexing/paginating from
        :param limit: maximum number of objects to send per pagination request"""
        result: OptionalDict = {"has_more": has_more, "data": list()}
        paginate_params = {"starting_after": starting_after, "limit": limit}

        if kwargs.get("params"):
            kwargs["params"].update(paginate_params)
        else:
            kwargs["params"] = paginate_params

        while has_more:
            req = self.req.get(url=url, **kwargs)
            response = req.json()
            result["data"].extend(response.get("data", list()))
            kwargs["params"]["starting_after"] = response["data"][-1].get("id")
            has_more = response.get("has_more", False)
            result["has_more"] = has_more

        return result

    def kwargs2params(self, func: Function, vals: RequiredDict, ignored_locals: ListString) -> RequiredDict:
        """Convert optional arguments in implemented API methods to dictionary values
        usable in the 'params' argument for various 'requests' HTTP methods. Ignores any keys that have the same
        name as any of the 'VALID_FILE_KEYS' as these are passed to underlying 'requests' HTTP methods using the
        'files' param for each relevant HTTP method.
        :param func: function to inspect
        :param vals: the values within the function, this is provided by calling 'locals()'
        :param ignored_locals: a list of strings of any local names to ignore, typically
                               this will be any required positionals passed to the function"""
        signature = inspect.signature(func)
        return {p.name: vals.get(p.name) for p in signature.parameters
                if p not in ignored_locals and vals.get(p.name) and vals.get(p.name) not in VALID_FILE_KEYS}
