import re
import subprocess

from pathlib import Path
from requests import Response
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import JSONDecodeError
from typing import Any, Optional

_function_kwargs: list[str] = ["ignore_statuses", "retry_statuses", "file_upload"]
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


class APIException(Exception):
    """Exception class for errors returned by the API."""
    pass


def api_error_check(r: Response) -> None:
    """Performs a check on the API response object for any error messages in the JSON body.
    :param r: requests.Response object"""
    api_errors = None

    try:
        api_errors = r.json().get("errors")
    except JSONDecodeError:
        pass
    finally:
        if api_errors is not None:
            err_strings = [f"'{err.get('title')}'" for err in api_errors if err.get("title")]

            raise APIException(f"SimpleMDM error/s: {', '.join(err_strings)}, HTTP {r.status_code}")


def urljoin(*paths, base: str, sep: Optional[str] = "/"):
    """Custom urljoin function because urllib.parse.urljoin is a bit dumb about multiple positional args.
    :param *paths: elements that form path locations
    :param base: the base url that paths are joined to, this should include the scheme; for example:
                       'https://example.org'
    :param sep: path seperator character; default is '/'"""
    fslash_reg = re.compile(rf"{sep}{2,}")  # pattern to make sure paths only have single '/'
    scheme_reg = re.compile(r":/{3,}")  # pattern to make sure scheme only has '://'
    paths = fslash_reg.sub(sep, f"{sep}".join(str(p) for p in paths if p))
    url = scheme_reg.sub("://", f"{base}{'/' if not base.endswith('/') else ''}{paths}")

    return url


def generate_url(self, *args) -> str:
    """Generate a URL from positional arguments.
    :param *args: positional arguments"""
    return urljoin(*[self.api_vers, self.endpoint, *args], base=self.BASE_URL)


def consume_kwargs(**kwargs) -> tuple[dict, dict]:
    """Consume keyword arguments and return a tuple containing a dict object representing request kwargs and a
    dict object representing function kwargs.
    The request kwargs are used for any 'requests.Session.request' call, and function kwargs are used for internal
    decorator function use.
    Any kwarg that is not a valid request kwarg or a valid function kwarg is discarded.
    :param **kwargs: keyword arguments"""
    rqst_kwargs, param_kwargs, func_kwargs = {}, {}, {}

    for k, v in kwargs.items():
        if k in _requests_kwargs:
            rqst_kwargs[k] = v
        elif k in _function_kwargs:
            func_kwargs[k] = v
        else:
            param_kwargs[k] = v

    # merge left over param kwargs
    rqst_kwargs["params"] = param_kwargs

    return rqst_kwargs, func_kwargs


def consume_func_kwargs(self, **kwargs) -> tuple[Any, ...]:
    """Consume function kwargs into a tuple of objects representing objects used in a decorator function.
    :param **kwargs: keyword arguments"""
    ignore = [*kwargs.get("ignore_statuses", []), *self.HTTP_IGNORE_STATUS_ERR]
    retry = [*kwargs.get("retry_statuses", []), *self.HTTP_RETRY_STATUS_LIST]

    return ignore, retry


def pkg_is_signed(pkg: Path) -> bool:
    """Determine if an installer package file is signed.
    :param pkg: path object"""
    cmd = ["/usr/sbin/pkgutil", "--check-signature", str(pkg)]
    p = subprocess.run(cmd, capture_output=True, encoding="utf-8")

    return p.returncode == 0 and "Status: no signature" not in p.stdout.strip()


def session_retry(self, retry: list[int]) -> HTTPAdapter:
    """Return an HTTPAdapter object that has a Retry instance attached.
    :param retry: list of HTTP status codes that trigger an automatic retry"""
    retries, forcelist, backoff = self.HTTP_MAX_RETRIES, retry, self.HTTP_RETRY_BACKOFF

    return HTTPAdapter(max_retries=Retry(total=retries, status_forcelist=forcelist, backoff_factor=backoff))
