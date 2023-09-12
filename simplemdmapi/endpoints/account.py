from requests.models import Response

from ..connector import SimpleMDMConnector
from .._decorators import param_kwargs, file_upload, url_suffixes
from .._validators import all_params, any_params

_param_kwargs = {
    "account.update": ["name", "apple_store_country_code"],
    "push_certificate.update": ["file", "apple_id"],
}

_param_opts_validation = {}


class Account(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#account"""

    def __init__(self, endpoint: str = "account", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    def show(self, **kwargs) -> Response:
        """Retrieve information about your account.
        Subscription information is only available for accounts on a manual billing plan."""
        return self.get(**kwargs)

    @any_params(_param_kwargs["account.update"])
    @param_kwargs(_param_kwargs["account.update"])
    def update(self, **kwargs) -> Response:
        """Update details about the account.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.patch(**kwargs)


class PushCertificate(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://api.simplemdm.com/#push-certificate"""

    def __init__(self, endpoint: str = "account", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    def certificate_info(self, **kwargs) -> Response:
        """Show details about the current push certificate."""
        return self.get(**kwargs)

    @all_params(["file"])
    @any_params(_param_kwargs["push_certificate.update"])
    @param_kwargs(_param_kwargs["apple_id"])
    @file_upload("file")
    def update(self, **kwargs) -> Response:
        """Upload a new push certificate, replacing the existing push certificate.
        :param file: string path representing the local file path to the certificate from the Apple Push
                     Certificates Portal
        :param apple_id: optional, email address of the Apple ID the push certificate was generated with"""
        # TODO - TEST UPLOADS!
        return self.post(**kwargs)

    @url_suffixes("scsr")
    def get_signed_csr(self, **kwargs) -> Response:
        """Download a signed certificate signing request from SimpleMDM.
        Note: the returned response should contain a base64 encoded property list for uploaded to the Apple Push
        Certificates Portal, the value of the 'data' key in this property list file can be uploaded to APCP as is."""
        return self.get(**kwargs)
