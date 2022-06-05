from .connector import SimpleMDMConnector
from .typehints import OptionalDict, UnionIntString
from typing import Any


class DEPServers(SimpleMDMConnector):
    """Simple MDM DEP Servers.
    https://simplemdm.com/docs/api/#dep-servers"""
    def __init__(self, endpoint: str = "dep_servers") -> None:
        self.endpoint = endpoint
        super().__init__()

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all DEP Servers.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs).json()  # Return list of server objects

    def list_devices(self, server_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all devices for the supplied DEP server.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/dep_devices"

        return self.paginate(url=url, params=params, **kwargs)  # Return list of device objects

    def retrieve(self, server_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve information about a dep_server.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{server_id}", params=params, **kwargs)  # Return server object

    def retrieve_device(self, server_id: UnionIntString, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve DEP device.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["include_awaiting_enrollment", "search"]
        url = f"{server_id}/dep_devices/{device_id}"

        return self.get(url=url, params=params, **kwargs)  # Return device object

    def sync(self, server_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Sync DEP server with Apple.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.post(url=f"{server_id}", params=params, **kwargs)  # Return ??
