from ..connector import SimpleMDMConnector
from typing import Any, Dict, Optional


class Logs(SimpleMDMConnector):
    """Logs.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#logs"""
    def __init__(self, endpoint: str = "logs") -> None:
        self.endpoint = endpoint
        super().__init__()

    def list_all(self, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """View logged events for device and admin interactions.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Return a list of log objects
