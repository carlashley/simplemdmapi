from .connector import SimpleMDMConnector
from .typehints import OptionalDict
from typing import Any


class Account(SimpleMDMConnector):
    """Simple MDM Account"""
    def __init__(self, endpoint: str = "account") -> None:
        self.endpoint = endpoint
        super().__init__()

    @SimpleMDMConnector.get()
    def show(self, params: OptionalDict, **kwargs) -> Any:
        """Retrieve information about your account.
        Subscription information is only available for accounts on a manual billing plan.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    @SimpleMDMConnector.patch()
    def update(self, params: OptionalDict, **kwargs) -> Any:
        """Update details about the account.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        self.validate_params(params, ["apple_store_country_code", "name"])
        return params, kwargs
