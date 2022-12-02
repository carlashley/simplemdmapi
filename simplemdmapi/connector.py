import inspect
import requests

from os import getenv
from pathlib import Path
from requests.adapters import HTTPAdapter, Retry
from time import monotonic, sleep
from typing import Any, Callable, Dict, List, Optional, Tuple


class SimpleMDMConnector:
    """SimpleMDM API Connector Class. Parent class for API endpoint calls."""
    BASE_URL = "https://a.simplemdm.com/api"
    HTTP_CONNECT_TIMEOUT: int = getenv("SIMPLEMDM_CONNECT_TIMEOUT") or 5
    HTTP_MAX_RETRIES: int = getenv("SIMPLEMDM_MAX_RETRIES") or 3
    HTTP_PAGINATE_MAX_RESULTS: int = getenv("SIMPLEMDM_RESULTS_PAGINATION") or 200
    HTTP_READ_TIMEOUT: int = getenv("SIMPLEMDM_READ_TIMEOUT") or 15
    HTTP_RETRY_BACKOFF: int = getenv("SIMPLEMDM_RETRY_BACKOFF") or 1
    HTTP_RETRY_STATUS_LIST: List[int] = [429, 500, 502, 503, 504]
    HTTP_IGNORE_STATUS_LIST: List[int] = [200, 201, 202]
    HTTP_SLEEP_WAIT: float = getenv("SIMPLEMDM_SLEEP_WAIT") or 1.0
    VALID_FILE_KEYS = ["binary", "file", "mobileconfig"]
    VALID_FILE_EXTS = [".mobileconfig", ".pkg", ".plist", ".txt"]

    TOKEN: Path | str = getenv("SIMPLEMDM_TOKEN") or Path("/var/root/simplemdm_token")
    RETRY: Retry = Retry(total=int(HTTP_MAX_RETRIES),
                         status_forcelist=HTTP_RETRY_STATUS_LIST,
                         backoff_factor=int(HTTP_RETRY_BACKOFF))

    if HTTP_SLEEP_WAIT:  # Convert to float
        HTTP_SLEEP_WAIT = float(HTTP_SLEEP_WAIT)

    def __init__(self,
                 version: str = "v1",
                 proxies: Optional[Dict[str, str]] = None) -> None:
        """Initialise the class with some core attributes.

        :param version: the API version string to use, default is 'v1'; this forms part of the full API url
        :param proxies: dictionary of proxy information to pass on to the session initialisation"""
        self.version = version
        self.session = self._initialise_session(proxies=proxies)
        self._attempt = 0  # internally track the attempts made
        self._last_req_ts = None  # timestamp for tracking rate limit requests

    def _clean_kwargs(self, kwargs: Dict[Any, Any]) -> Dict[Any, Any]:
        """Cleans a dictionary of 'keyword' arguments by removing keys that are not part of the standard
        'requests.request' API parameters."""
        keep_args = ["method",
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
                     "json"]

        for k, _ in kwargs.copy().items():
            if k not in keep_args:
                try:
                    del kwargs[k]
                except KeyError:
                    pass

        return kwargs

    def _initialise_session(self,
                            adapter_protocols: List[str] = ["https://"],
                            proxies: Optional[Dict[str, str]] = None) -> requests.Session:
        """Initialise an instance of the 'requests.Session'.

        :param adapter_protocols: list of protocols (as str) to mount the HTTPAdapter to
        :param proxies: dictionary of proxy information to apply to the session instance"""
        s = requests.Session()

        if proxies:
            s.proxies.update(proxies)

        # Mount the HTTP adapter for handling retries, etc
        for protocol in adapter_protocols:
            s.mount(protocol, HTTPAdapter(max_retries=self.RETRY))

        # Authorise
        s.auth = requests.auth.HTTPBasicAuth(self._read_token(self.TOKEN), '')

        return s

    def _k2p(self,
             func: Callable,
             vals: Dict[Any, Any],
             ignored_locals: List[str],
             rename_keys: Optional[Dict[Any, Any]] = dict()) -> Dict[Any, Any]:
        """Converts optional arguments from internal model methods into parameters that can be sent via each REST
        HTTP call. The argument names must match the parameters that are used in each respective SimpleMDM API method.

        Certain arguments/parameters are ignored if they're in the 'VALID_FILE_KEYS' as they're passed to the underlyng
        'requests' HTTP methods that accept the 'files' parameter (i.e. PUT/POST type requests).

        :param func: function to inspect
        :param vals: the values within the function, this is provided by calling 'locals()'
        :param ignored_locals: a list of strings of any local names to ignore, typically
                               this will be any required positionals passed to the function
        :param rename_keys: a dictionary 'key: value' that indicates a param passed in by an internal method must
                            be renamed to the correct key, for example, if a param name clashes with a reserved Python
                            word/type, such as: '{'fmt': 'format'}' would rename 'fmt' to the API param 'format' which
                            is a reserved word in Python"""
        ignored_locals = set(ignored_locals)
        ignored_locals.add("params")
        signature = inspect.signature(func)
        result = dict()

        for param in signature.parameters:
            name = rename_keys.get(param, param)  # default to original param name if not in 'rename_keys'
            value = vals.get(name)

            if value and param not in ignored_locals:  # check original param name is not in 'ignored_locals'
                result[name] = value

        return result

    def _prepare_args(self, url: Optional[str] = None, **kwargs) -> Tuple[Any, ...]:
        """Creates a full URL string from the provided URL and the API URL path and cleans up keyword arguments for
        use in any 'requests.Session.method()' call.

        Returns a dataclass object with all the various cleaned up arguments.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        url = self._urljoin(self.BASE_URL, self.version, self.endpoint, url)
        i_s = kwargs.get("ignore_statuses", list())
        i_s.extend(self.HTTP_IGNORE_STATUS_LIST)  # merge with default ignore status codes
        i_s = list(set(i_s))  # Uniqify
        r_s = kwargs.get("retry_statuses", list())
        r_s.extend(self.HTTP_RETRY_STATUS_LIST)  # merge with default retry status codes
        r_s = list(set(r_s))  # Uniqify
        kwargs["timeout"] = kwargs.get("timeout", self.HTTP_CONNECT_TIMEOUT)
        kwargs = self._clean_kwargs(kwargs)

        return (url, i_s, r_s, kwargs)

    def _read_token(self, t: Path | str) -> Optional[str]:
        """Pass in the token for authentication purposes. If the token string is a file path, read the file and
        return the token contents as a string.

        When the token is stored as a file, the token must be stored in the file without any new line/carriage returns.
        Note: When storing the token as a file, please ensure the permissions of the file are such that it can only
              be read by the user/group of the account that this API tool runs as.

        :param t: the token as a string, or as a file path (as a string)"""
        fp = Path(t)

        if fp.is_file() and fp.exists():
            with fp.open("r") as f:
                return "".join(f.readlines()).strip()
        else:
            return t

    def _should_sleep(self, _mt: float = monotonic()) -> bool:
        """Check if there should be a sleep between each request being sent.

        :param _mt: monotonic time value"""
        if self._last_req_ts:
            last_req_delta = _mt - self._last_req_ts
            self._last_req_ts = monotonic()

            return last_req_delta < self.HTTP_SLEEP_WAIT

        return False

    def _session_method(self, method: str, url: Optional[str] = None, **kwargs) -> Optional[requests.models.Response]:
        """Performs the specified method action using the constructed session.

        :param method: valid HTTP method; for example:  'DELETE', 'GET', 'PATCH', 'POST', 'PUT'.
        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        method = method.upper()  # Just in case.
        upload_key = None

        if method in ["POST", "PUT"] and kwargs.get("files"):  # Handle methods that can post/put files
            upload_key = kwargs.get("upload_key")

        url, ignore_statuses, retry_statuses, kwargs = self._prepare_args(url=url, **kwargs)

        if method in ["POST", "PUT"] and kwargs.get("files"):  # Performing an upload, so handle this specifically
            fp = Path(kwargs["files"][upload_key])

            with fp.open("rb") as f:
                kwargs["files"][upload_key] = f
                req = self.session.request(method=method, url=url, **kwargs)
        else:
            req = self.session.request(method=method, url=url, **kwargs)

        # Retry but only if the status code slips through the inbuilt session retry configuration.
        if req.status_code in retry_statuses:
            # if self._attempt < self.HTTP_MAX_RETRIES:
            while self._attempt < self.HTTP_MAX_RETRIES:
                if self._should_sleep():
                    sleep(self.HTTP_SLEEP_WAIT)

                self._session_method(method=method, url=url, kwargs=kwargs)  # pass original values through
                self._attempt += 1

            self._attempt = 0  # ensure reset attempt count occurs on success
            self._last_req_ts = None  # ensure last request timestamp is reset on success

        # Raise exceptions if necessary, ignores any status codes that are safe to ignore,
        # as some of the API methods return status codes that would technically be considered
        # 'bad' but are just a way of flagging that action was or was not taken.
        if req.status_code not in ignore_statuses:
            req.raise_for_status()

        return req

    def _urljoin(self, *args) -> str:
        """Returns the input list of 'arguments' as a URL string."""
        return "/".join([x.strip("/") for x in args if x])

    # Public methods
    def delete(self, url: Optional[str] = None, **kwargs) -> Optional[requests.models.Response]:
        """Executes the HTTP 'DELETE' method.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        return self._session_method(method="DELETE", url=url, **kwargs)

    def get(self, url: Optional[str] = None, **kwargs) -> Optional[requests.models.Response]:
        """Executes the HTTP 'GET' method.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        return self._session_method(method="GET", url=url, **kwargs)

    def patch(self, url: Optional[str] = None, **kwargs) -> Optional[requests.models.Response]:
        """Executes the HTTP 'PATCH' method.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        return self._session_method(method="PATCH", url=url, **kwargs)

    def post(self, url: Optional[str] = None, **kwargs) -> Optional[requests.models.Response]:
        """Executes the HTTP 'POST' method.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        return self._session_method(method="POST", url=url, **kwargs)

    def put(self, url: Optional[str] = None, **kwargs) -> Optional[requests.models.Response]:
        """Executes the HTTP 'PUT' method.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'"""
        return self._session_method(method="PUT", url=url, **kwargs)

    def paginate(self,
                 url: Optional[str] = None,
                 start: int = 0,
                 limit: int = 100,
                 has_more: bool = True,
                 **kwargs) -> Optional[Dict[Any, Any]]:
        """Paginate results for API endpoint methods that require pagination.

        :param url: optional URL string, do not provide the full URL, only provide the components after the
                    specific endpoint being called; for example, 'id/lock' or 'id/users/user_id'
        :param start: record to start pagination from
        :param limit: maximum number of results per pagination request
        :param has_more: boolean value to indicate if pagination should continue or not, initially defaults
                         to True, but will flipped to False by this method as required to stop paginating"""
        result = {"has_more": has_more, "data": list()}
        paginate_params = {"starting_after": start, "limit": limit}

        if kwargs.get("params"):
            kwargs["params"].update(paginate_params)
        else:
            kwargs["params"] = paginate_params

        while has_more:
            req = self.get(url=url, **kwargs)
            response = req.json()
            result["data"].extend(response.get("data", list()))
            kwargs["params"]["starting_after"] = response["data"][-1].get("id")
            has_more = response.get("has_more", False)
            result["has_more"] = has_more

        return result
