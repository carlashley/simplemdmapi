from pathlib import Path
from typehints import RequiredDict, UnionStringPath


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
