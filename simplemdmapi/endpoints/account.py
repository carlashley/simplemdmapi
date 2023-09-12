from requests.models import Response

from ..connector import SimpleMDMConnector
from .._decorators import param_kwargs
from .._validators import any_params

_param_kwargs = {
    "update": ["name", "apple_store_country_code"],
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

    @any_params(_param_kwargs["update"])
    @param_kwargs(_param_kwargs["update"])
    def update(self, **kwargs) -> Response:
        """Update details about the account.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.patch(**kwargs)
