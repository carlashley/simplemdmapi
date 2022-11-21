from ..connector import SimpleMDMConnector
from typing import Any, Optional


class Logs(SimpleMDMConnector):
    """Logs.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#logs"""
    def __init__(self, endpoint: str = "logs") -> None:
        self.endpoint = endpoint
        super().__init__()

    def list_all(self, serial: Optional[str] = None, **kwargs) -> Any:
        """View logged events for device and admin interactions.

        :param serial: limit response data to the logs of a single device, no value returns all logs
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.list_all, vals=locals(), ignored_locals=list())
        return self.paginate(params=params, **kwargs)  # Return a list of log objects
