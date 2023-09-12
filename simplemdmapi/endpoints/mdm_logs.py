from requests.models import Response
from typing import Generator

from ..connector import SimpleMDMConnector
from .._decorators import paginate, param_kwargs

_param_kwargs = {
    "list_all": [
        "serial_number",
        "starting_after",
        "limit",
    ],
}

_param_opts_validation = {}


class Logs(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://api.simplemdm.com/#logs"""

    def __init__(self, endpoint: str = "logs", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @param_kwargs(_param_kwargs["list_all"])
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all logs.
        :param serial_number: optional, search for logs by serial number
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: device id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    def retrieve(self, log_id: str, **kwargs) -> Response:
        """Retrieve one log entry.
        :param log_id: id of the log entry"""
        return self.get(f"{log_id}", **kwargs)
