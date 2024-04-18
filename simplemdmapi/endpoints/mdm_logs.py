from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate


class Logs(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://api.simplemdm.com/#logs"""

    def __init__(self, endpoint: str = "logs", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
        }

    @method_params
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
        return self.get(log_id, **kwargs)
