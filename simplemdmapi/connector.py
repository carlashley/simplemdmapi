"""Connection class."""
import requests

from os import getenv
from pathlib import Path
from typing import Optional
from keychain import read_password

from ._decorators import request
from ._mixins import StatusesMixin, TokenMixin


class SimpleMDMConnector(StatusesMixin, TokenMixin):
    """Connection class to connect to SimpleMDM."""
    BASE_URL: str = "https://a.simplemdm.com/api"
    HTTP_PAGINATE_MAX_RESULTS: int = int(getenv("SIMPLEMDM_RESULTS_PAGINATION", 200))
    HTTP_CONNECT_TIMEOUT: int = int(getenv("SIMPLEMDM_CONNECT_TIMEOUT", 5))
    HTTP_READ_TIMEOUT: int = int(getenv("SIMPLEMDM_READ_TIMEOUT", 5))
    HTTP_MAX_RETRIES: int = int(getenv("SIMPLEMDM_MAX_RETRIES", 3))
    HTTP_RETRY_BACKOFF: int = int(getenv("SIMPLEMDM_RETRY_BACKOFF", 1))
    HTTP_SLEEP_WAIT: float = float(getenv("SIMPLEMDM_SLEEP_WAIT", 1.0))
    HTTP_RETRY_STATUS_LIST: list[int] = [429, 500, 502, 503, 504]
    HTTP_IGNORE_STATUS_ERR: list[int] = [200, 201, 202]
    DEFAULT_AUTH_TOKEN_PATH: Path = Path("/var/root/simplemdm_token")
    _TOKEN: str | Path = getenv("SIMPLEMDM_TOKEN", DEFAULT_AUTH_TOKEN_PATH)

    def __init__(self, api_vers: str = "v1", tkn: Optional[str | Path] = None, proxies: Optional[dict] = {}) -> None:
        """Initialise class."""
        self.api_vers = api_vers
        self.session = self._initialise_session(proxies)

    def _initialise_session(self, tkn: str | Path, proxies: Optional[dict] = {}) -> requests.Session:
        """Initialise a requests.Session instance for qeuries.
        :param proxies: optional dictionary object representing a proxy configuration."""
        session = requests.Session()
        session.proxies.update(proxies)
        session.auth = requests.auth.HTTPBasicAuth(read_password("simplemdmapi-full"), "")

        return session

    @request("delete")
    def delete(self, *args, **kwargs):
        """DELETE request method.
        Usage: self.delete(url)
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("get")
    def get(self, *args, **kwargs):
        """GET request method.
        Usage: self.get(url)
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("patch")
    def patch(self, *args, **kwargs):
        """PATCH request method.
        Usage: self.patch(url, id="1", binary="/path/to/app.pkg", "name": "HelloWorld")
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("post")
    def post(self, *args, **kwargs):
        """POST request method.
        Usage: self.post(url, id="1", binary="/path/to/app.pkg", "name": "HelloWorld")
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return

    @request("put")
    def put(self, *args, **kwargs):
        """PUT request method.
        Usage: self.put(url, id="1", binary="/path/to/app.pkg", "name": "HelloWorld")
        :param *args: non keyword arguments
        :param **kwargs: keyword arguments"""
        return
