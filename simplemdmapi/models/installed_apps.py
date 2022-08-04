from ..api import SimpleMDMConnector
from ..typehints import OptionalDict, UnionIntString
from typing import Any


class InstalledApps(SimpleMDMConnector):
    """Installed Apps.

    Note: Listing apps on a device is implemented in the 'devices' model.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#installed-apps
    """
    def __init__(self, endpoint: str = "installed_apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def retrieve(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Show details of an installed app.

        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{app_id}", params=params, **kwargs)  # Return an installed app object

    def request_management(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Request management of an unmanaged app installed on a device.

        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/request_management"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def install_update(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Install app update for an installed app on devices assigned the app.

        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/update"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def uninstall(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Uninstall an installed app.

        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{app_id}", params=params, **kwargs)  # Return 202 status
