from pathlib import Path
from typing import Optional
from requests.models import Response

from .. import SimpleMDMConnector
from ..decorators import method_params, url_suffixes


class Account(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#account"""

    def __init__(self, endpoint: str = "account", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "update": {
                "all_params": ["name", "apple_store_country_code"],
                "any_params": ["name", "apple_store_country_code"],
            },
        }

    def show(self, **kwargs) -> Response:
        """Retrieve information about your account.
        Subscription information is only available for accounts on a manual billing plan."""
        return self.get(**kwargs)

    @method_params
    def update(self, **kwargs) -> Response:
        """Update details about the account.
        :param name: name of the account
        :param apple_store_country_code: the app store country code to use, for example: 'AU'"""
        return self.patch(**kwargs)


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
