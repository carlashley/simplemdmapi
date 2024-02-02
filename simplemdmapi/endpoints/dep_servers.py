from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate, url_suffixes


class DEPServers(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#dep-servers"""

    def __init__(self, endpoint: str = "dep_servers", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {}

    def list_all(self, **kwargs) -> Response:
        """List all DEP servers."""
        return self.get(**kwargs)

    def retrieve(self, server_id: str, **kwargs) -> Response:
        """Retrieve one DEP Server.
        :param server_id: the DEP server id"""
        return self.get(server_id, **kwargs)

    @url_suffixes("sync")
    def sync_with_apple(self, server_id: str, **kwargs) -> Response:
        """Sync a DEP Server with Apple.
        :param server_id: the DEP server id"""
        return self.post(server_id, **kwargs)


class DEPDevices(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#dep-servers"""

    def __init__(self, endpoint: str = "dep_servers", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "retrieve": {
                "all_params": ["device_id"],
                "req_params": ["device_id"],
            },
        }

    @url_suffixes("dep_devices")
    @paginate
    def list_all(self, server_id: str, **kwargs) -> Generator[dict, None, None]:
        """List all DEP devices associated with a DEP server.
        :param server_id: the DEP server id"""
        return self.get(server_id, **kwargs)

    @method_params
    @url_suffixes("dep_devices", ["device_id"])
    def retrieve(self, server_id: str, **kwargs) -> Response:
        """Retrieve one device associated with a DEP Server.
        :param server_id: the DEP server id"""
        return self.get(server_id, **kwargs)


class PushCertificate(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://api.simplemdm.com/#push-certificate"""

    def __init__(
        self, endpoint: str = "push_certificate", dry_run: bool = False, tkn: Optional[str | Path] = None
    ) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "update": {
                "all_params": ["file", "apple_id"],
                "req_params": ["file"],
                "file_param": "file",
            },
        }

    def certificate_info(self, **kwargs) -> Response:
        """Show details about the current push certificate."""
        return self.get(**kwargs)

    @method_params
    def push_certificate_update(self, **kwargs) -> Response:
        """Upload a new push certificate, replacing the existing push certificate.
        :param file: string path representing the local file path to the certificate from the Apple Push
                     Certificates Portal
        :param apple_id: optional, email address of the Apple ID the push certificate was generated with"""
        return self.post(**kwargs)

    @url_suffixes("scsr")
    def get_signed_csr(self, **kwargs) -> Response:
        """Download a signed certificate signing request from SimpleMDM.
        Note: the returned response should contain a base64 encoded property list for uploaded to the Apple Push
        Certificates Portal, the value of the 'data' key in this property list file can be uploaded to APCP as is."""
        return self.get(**kwargs)
