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
        return self.paginate(params=params, **kwargs)  # Return list of server objects

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
        url = f"{server_id}/sync"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status


class PushCertificates(SimpleMDMConnector):
    """Simple MDM Push Certificates.
    https://simplemdm.com/docs/api/#push-certificate"""
    def __init__(self, endpoint: str = "push_certificate") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_csr(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Generate a signed CSR for the Apply Push Certificates portal.
        The certificate is returned in the 'data' key, and can be uploaded as is.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url="scsr", params=params, **kwargs).json()

    def show(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Show details of the current push certificate.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(params=params, **kwargs).json()  # Return push certificate details object

    def update(self, params: OptionalDict = dict(), files: OptionalDict = dict(), **kwargs) -> Any:
        """Upload a new certificate (replaces the existing certificate).
        :param params: specific parameters to provide to the API query.
        :param files: specific files to upload; example: {"binary": "/tmp/updatedpackage.pkg"}
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["apple_id"]

        return self.put(params=params, files=files, **kwargs).json()  # Return certificate details object
