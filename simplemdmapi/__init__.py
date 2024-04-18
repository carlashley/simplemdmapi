"""This is a Python implementation of the SimpleMDM API:
    https://api.simplemdm.com/#introduction"""

__author__ = "Carl Ashley"
__name__ = "simplemdmapi"
__version__ = "1.0.20230923"

import requests

from os import getenv
from pathlib import Path
from typing import Optional

from .decorators import request


class SimpleMDMConnector:
    """Connection class to connect to SimpleMDM."""

    BASE_URL: str = "https://a.simplemdm.com/api"
    HTTP_PAGINATE_MAX_RESULTS: int = int(getenv("SIMPLEMDM_RESULTS_PAGINATION", 200))
    HTTP_CONNECT_TIMEOUT: int = int(getenv("SIMPLEMDM_CONNECT_TIMEOUT", 5))
    HTTP_READ_TIMEOUT: int = int(getenv("SIMPLEMDM_READ_TIMEOUT", 5))
    HTTP_MAX_RETRIES: int = int(getenv("SIMPLEMDM_MAX_RETRIES", 3))
    HTTP_RETRY_BACKOFF: int = int(getenv("SIMPLEMDM_RETRY_BACKOFF", 1))
    HTTP_SLEEP_WAIT: float = float(getenv("SIMPLEMDM_SLEEP_WAIT", 1.0))
    HTTP_RETRY_STATUS_LIST: list[int] = [429, 500, 502, 503, 504]
    HTTP_IGNORE_STATUS_ERR: list[int] = [200, 201, 202, 500]
    DEFAULT_AUTH_TOKEN_PATH: Path = Path("/var/root/simplemdm_token")
    _TOKEN: str | Path = getenv("SIMPLEMDM_TOKEN", DEFAULT_AUTH_TOKEN_PATH)

    def __init__(self, api_vers: str = "v1", tkn: Optional[str | Path] = None, proxies: Optional[dict] = {}) -> None:
        """Initialise class."""
        self.api_vers = api_vers
        self.tkn = tkn or self._TOKEN
        self.session = self._initialise_session(proxies)

    def _initialise_session(self, tkn: str | Path, proxies: Optional[dict] = {}) -> requests.Session:
        """Initialise a requests.Session instance for qeuries.
        :param proxies: optional dictionary object representing a proxy configuration."""
        session = requests.Session()
        session.proxies.update(proxies)
        session.auth = requests.auth.HTTPBasicAuth(self._read_token(self.tkn), "")

        return session

    def _token_is_file(self, tkn: str | Path) -> bool:
        """Return True/False if the token is a file object and exists.
        :param tkn: path object"""
        tkn = Path(tkn)
        return tkn.is_file() and tkn.exists()

    def _read_token(self, tkn: Path, _mode: str = "rb", _enc: str = "utf-8") -> str:
        """Read the token from a file object.
        :param tkn: path object"""
        if self._token_is_file(tkn):
            with tkn.open(_mode, encoding=_enc) as f:
                return f.read().strip()
        else:
            return tkn.strip()

    @request("delete")
    def delete(self, *args, **kwargs):
        """DELETE request method.
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("get")
    def get(self, *args, **kwargs):
        """GET request method.
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("patch")
    def patch(self, *args, **kwargs):
        """PATCH request method.
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("post")
    def post(self, *args, **kwargs):
        """POST request method.
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("put")
    def put(self, *args, **kwargs):
        """PUT request method.
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return
