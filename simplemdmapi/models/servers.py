from ..connector import SimpleMDMConnector
from typing import Any, Dict, Optional


class DEPServers(SimpleMDMConnector):
    """DEP Servers.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#dep-servers
    """
    def __init__(self, endpoint: str = "dep_servers") -> None:
        self.endpoint = endpoint
        super().__init__()

    def list_all(self, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """List all DEP Servers.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Return list of server objects

    def list_devices(self, server_id: int | str, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """List all devices for the supplied DEP server.

        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/dep_devices"

        return self.paginate(url=url, params=params, **kwargs)  # Return list of device objects

    def retrieve(self, server_id: int | str, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """Retrieve information about a dep_server.

        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{server_id}", params=params, **kwargs)  # Return server object

    def retrieve_device(self,
                        server_id: int | str,
                        device_id: int | str,
                        params: Optional[Dict[Any, Any]] = dict(),
                        **kwargs) -> Any:
        """Retrieve DEP device.

        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/dep_devices/{device_id}"

        return self.get(url=url, params=params, **kwargs)  # Return device object

    def sync(self, server_id: int | str, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """Sync DEP server with Apple.

        :param server_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/sync"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status


class PushCertificates(SimpleMDMConnector):
    """Push Certificates.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#push-certificate
    """
    def __init__(self, endpoint: str = "push_certificate") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_csr(self, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """Generate a signed CSR for the Apply Push Certificates portal.

        The certificate is returned in the 'data' key, and can be uploaded as is.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url="scsr", params=params, **kwargs).json()

    def show(self, params: Optional[Dict[Any, Any]] = dict(), **kwargs) -> Any:
        """Show details of the current push certificate.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(params=params, **kwargs).json()  # Return push certificate details object

    def update(self,
               params: Optional[Dict[Any, Any]] = dict(),
               files: Optional[Dict[Any, Any]] = dict(),
               **kwargs) -> Any:
        """Upload a new certificate (replaces the existing certificate).

        :param params: specific parameters to provide to the API query.
        :param files: specific files to upload; example: {"binary": "/tmp/updatedpackage.pkg"}
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.put(params=params, files=files, **kwargs).json()  # Return certificate details object
