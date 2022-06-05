from .connector import SimpleMDMConnector
from .typehints import (OptionalDict,
                        UnionIntString)
from typing import Any


class DEPServers(SimpleMDMConnector):
    """Simple MDM DEP Servers"""
    def __init__(self, endpoint: str = "dep_servers") -> None:
        self.endpoint = endpoint
        super().__init__()

    @SimpleMDMConnector.paginate()
    def list_all(self, params: OptionalDict, **kwargs) -> Any:
        """List all DEP Servers.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    def list_devices(self, server_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """List all DEP Servers.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/dep_devices"

        return SimpleMDMConnector.get(url=url)(lambda _: (params, kwargs))(self)

    @SimpleMDMConnector.get()
    def retrieve(self, params: OptionalDict, **kwargs) -> Any:
        """Retrieve information about a dep_server.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    def retrieve_device(self, server_id: UnionIntString, device_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Retrieve DEP device.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["include_awaiting_enrollment", "search"]

        if params:
            self.validate_params(params, valid_params)

        url = f"{server_id}/dep_devices/{device_id}"

        return SimpleMDMConnector.get(url=url)(lambda _: (params, kwargs))(self)

    def sync(self, server_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Sync DEP server with Apple.
        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return SimpleMDMConnector.post(url=server_id)(lambda _: (params, kwargs))(self)
