from .connector import SimpleMDMConnector, APIParamException
from .typehints import OptionalDict, UnionIntString
from typing import Any


class Apps(SimpleMDMConnector):
    """Simple MDM Apps.
    https://simplemdm.com/docs/api/#apps"""
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, params: OptionalDict = dict(), files: OptionalDict = dict(), **kwargs) -> Any:
        """Upload/create an app.
        :param params: specific parameters to provide to the API query.
        :param files: file to upload (optional).
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["app_store_id", "bundle_id", "binary", "name"]
        kwargs["unique_params"] = ["app_store_id", "bundle_id", "binary"]

        if params.get("name") and not params.get("binary"):
            raise APIParamException("Error: 'name' parameter cannot be used without 'binary' parameter.")

        return self.post(params=params, files=files, **kwargs).json()  # Return created app object

    def delete_app(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an app.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{app_id}", params=params, **kwargs)  # Return 204 status

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all applications.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        self.paginate(params=params, **kwargs)  # Return list of app objects

    def list_installs(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all applications.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/installs"

        return self.paginate(url=url, params=params, **kwargs)  # Return list of app install objects

    def retrieve(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve one application.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{app_id}", params=params, **kwargs).json()  # Return app object

    def update(self, app_id: UnionIntString, params: OptionalDict = dict(), files: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about an app.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param files: specific files to upload; example: {"binary": "/tmp/updatedpackage.pkg"}
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["binary", "deploy_to", "name"]

        return self.patch(url=f"{app_id}", params=params, files=files, **kwargs).json()  # Return app update object


class ManagedAppConfigs(SimpleMDMConnector):
    """Simple Managed App Configs.
    https://simplemdm.com/docs/api/#managed-app-configs"""
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_config(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve managed application configuration.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/managed_configs"

        return self.get(url=url, params=params, **kwargs).json()  # Return app object

    def create(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Create a managed app config.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["key", "value", "value_type"]
        kwargs["required_params"] = ["key"]
        url = f"{app_id}/managed_configs"

        return self.post(url=url, params=params, **kwargs).json()  # Return created app object

    def delete(self, app_id: UnionIntString, config_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete a managed config for an app.
        :param app_id: the id value.
        :praam config_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/managed_configs/{config_id}"

        return self.delete(url=url, params=params, **kwargs)  # Return 204 status

    def push_updates(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Push a managed config for an app to all devices with that app.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/managed_configs/push"

        return self.patch(url=url, params=params, **kwargs).json()  # Return app update object
