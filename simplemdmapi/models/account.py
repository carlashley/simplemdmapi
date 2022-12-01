from typing import Optional
from requests.models import Response
from ..connector import SimpleMDMConnector


class Account(SimpleMDMConnector):
    """Account.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#account
    """
    def __init__(self, endpoint: str = "account") -> None:
        self.endpoint = endpoint
        super().__init__()

    def show(self, **kwargs) -> Response:
        """Retrieve information about your account.

        Subscription information is only available for accounts on a manual billing plan."""
        return self.get(**kwargs)

    def update(self, name: Optional[str] = None, apple_store_country_code: Optional[str] = None, **kwargs) -> Response:
        """Update details about the account.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.update, vals=locals(), ignored_locals=list())
        return self.patch(params=params, **kwargs)
