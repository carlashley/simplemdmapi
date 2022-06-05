from .connector import SimpleMDMConnector
from .typehints import OptionalDict
from typing import Any


class Account(SimpleMDMConnector):
    """Simple MDM Account.
    https://simplemdm.com/docs/api/#account"""
    def __init__(self, endpoint: str = "account") -> None:
        self.endpoint = endpoint
        super().__init__()

    def show(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve information about your account.
        Subscription information is only available for accounts on a manual billing plan.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(params=params, **kwargs).json()  # Return json content of account info

    def update(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about the account.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["valid_params"] = ["apple_store_country_code", "name"]
        return self.get(params=params, **kwargs).json()  # Return json content of updated account info
