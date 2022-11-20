from ..connector import SimpleMDMConnector
from typing import Any, Optional


class Account(SimpleMDMConnector):
    """Account.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#account
    """
    def __init__(self, endpoint: str = "account") -> None:
        self.endpoint = endpoint
        super().__init__()

    def show(self, **kwargs) -> Any:
        """Retrieve information about your account.

        Subscription information is only available for accounts on a manual billing plan."""
        return self.get(**kwargs).json()  # Return json content of account info

    def update(self, name: Optional[str] = None, country_code: Optional[str] = None, **kwargs) -> Any:
        """Update details about the account.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.update, locals(), ["params"])
        return self.patch(params=params, **kwargs).json()  # Return json content of updated account info
