from ..connector import SimpleMDMConnector
from typing import Any, Optional


class DEPServers(SimpleMDMConnector):
    """DEP Servers.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#dep-servers
    """
    def __init__(self, endpoint: str = "dep_servers") -> None:
        self.endpoint = endpoint
        super().__init__()

    def list_all(self, **kwargs) -> Any:
        """List all DEP Servers.

        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(**kwargs)  # Return list of server objects

    def list_devices(self,
                     search: Optional[str] = None,
                     include_awaiting_enrollment: Optional[bool] = False,
                     include_secret_custom_attributes: Optional[bool] = False,
                     **kwargs) -> Any:
        """List all devices for the specified DEP/ADE server.

        :param server_id: the id value.
        :param search: limit result response to devices that match the optional string value (searches on
                       name, UDID, serial, IMEI, MAC address, or phone number)
        :param include_awaiting_enrolment: include devices that are waiting to be enrolled (default is False)
        :param include_secret_custom_attributes: include ALL custom attributes including those marked
                                                 as secret (default is False)
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.list_all, vals=locals(), ignored_locals=list())
        return self.paginate(params=params, **kwargs)  # Return list of device objects in the DEP/ADE server

    def retrieve(self, server_id: int | str, **kwargs) -> Any:
        """Retrieve information about a dep_server.

        :param server_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{server_id}", **kwargs)  # Return server object

    def retrieve_device(self,
                        server_id: int | str,
                        device_id: int | str,
                        **kwargs) -> Any:
        """Retrieve DEP device.

        :param server_id: the id value.
        :param device_id: the device id.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/dep_devices/{device_id}"

        return self.get(url=url, **kwargs)  # Return device object

    def sync(self, server_id: int | str, **kwargs) -> Any:
        """Sync DEP server with Apple.

        :param server_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{server_id}/sync"

        return self.post(url=url, **kwargs)  # Return 202 status


class PushCertificates(SimpleMDMConnector):
    """Push Certificates.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#push-certificate
    """
    def __init__(self, endpoint: str = "push_certificate") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_csr(self, **kwargs) -> Any:
        """Generate a signed CSR for the Apply Push Certificates portal.

        The certificate is returned in the 'data' key, and can be uploaded as is.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url="scsr", **kwargs).json()

    def show(self, **kwargs) -> Any:
        """Show details of the current push certificate.

        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(**kwargs).json()  # Return push certificate details object

    def update(self,
               file: str,
               apple_id: Optional[str] = None,
               **kwargs) -> Any:
        """Upload a new certificate (replaces the existing certificate).

        :param params: specific parameters to provide to the API query.
        :param file: specific file to upload; example: {"binary": "/tmp/updatedpackage.pkg"}
        :param kwargs: specific parameters to provide to the underlying requests function."""
        files = {"file": file}
        params = self._k2p(self.update, vals=locals(), ignored_locals=list())
        return self.put(params=params, files=files, upload_key="file", **kwargs).json()
