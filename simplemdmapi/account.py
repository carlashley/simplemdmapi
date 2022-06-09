from .connector import SimpleMDMConnector
from .typehints import OptionalString
from typing import Any


class Account(SimpleMDMConnector):
    """Simple MDM Account.
    https://simplemdm.com/docs/api/#account"""
    def __init__(self, endpoint: str = "account") -> None:
        self.endpoint = endpoint
        super().__init__()

    def show(self) -> Any:
        """Retrieve information about your account.
        Subscription information is only available for accounts on a manual billing plan.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get().json()  # Return json content of account info

    def update(self, name: OptionalString = None, country_code: OptionalString = None) -> Any:
        """Update details about the account.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self.kwargs2params(self.update, locals(), ["params"])
        return self.patch(params=params).json()  # Return json content of updated account info
