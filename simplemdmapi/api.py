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
from .utils import clean_kwargs, read_token, urljoin
from os import getenv
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry

try:
    from .proxies import proxy_settings
except ImportError:
    proxy_settings = None
    pass

# TO DO - 2022-08-04-215:
# - check if the 'required_params' and 'validate_params' in 'validators' is required
# - move items in 'validators' into 'utils'

HTTP_TIMEOUTS: TupleInt = (5, 15)
HTTP_MAX_RETRIES: int = 3
HTTP_RETRY_BACKOFF: int = 1
HTTP_RETRY_STATUSES: ListInt = [429, 500, 502, 503, 504]


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
    def __init__(self,
                 token: UnionStringPath = getenv("SIMPLETOKEN"),
                 base_url: str = "https://a.simplemdm.com/api/v1",
                 timeout: TupleInt = HTTP_TIMEOUTS,
                 max_retry: int = HTTP_MAX_RETRIES,
                 retry_backoff: int = HTTP_RETRY_BACKOFF,
                 http_status_retries: ListInt = HTTP_RETRY_STATUSES) -> None:
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
        """Pre parse all internal HTTP request methods.

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'"""
        url = urljoin(self.base_url, self.endpoint, url)
        ignore_statuses = kwargs.get("ignore_statuses", list())
        kwargs = clean_kwargs(kwargs)
        kwargs["timeout"] = kwargs.get("timeout", self.timeout)

        return url, ignore_statuses, kwargs

    def delete(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """DELETE

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'"""
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = self.session.delete(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def get(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """GET

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'"""
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = self.session.get(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def patch(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """PATCH

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'"""
        url, ignore_statuses, kwargs = self._parser(url=url, **kwargs)
        req = self.session.patch(url, **kwargs)

        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def post(self, url: OptionalString = None, **kwargs) -> RequestsResponse:
        """POST

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'"""
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
        """PUT

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'"""
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

        :param url: optional URL string, anything provided in this param will be automatically joined to the
                    class attribute 'base_url'
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
        """Converts optional arguments from internal model methods into parameters that can be sent via each REST
        HTTP call. The argument names must match the parameters that are used in each respective SimpleMDM API method.

        Certain arguments/parameters are ignored if they're in the 'VALID_FILE_KEYS' as they're passed to the underlyng
        'requests' HTTP methods that accept the 'files' parameter (i.e. PUT/POST type requests).

        :param func: function to inspect
        :param vals: the values within the function, this is provided by calling 'locals()'
        :param ignored_locals: a list of strings of any local names to ignore, typically
                               this will be any required positionals passed to the function"""
        ignored_locals = set(ignored_locals)
        ignored_locals.add("params")
        signature = inspect.signature(func)

        return {p.name: vals.get(p.name) for p in signature.parameters
                if p not in ignored_locals and vals.get(p.name) and vals.get(p.name) not in VALID_FILE_KEYS}
