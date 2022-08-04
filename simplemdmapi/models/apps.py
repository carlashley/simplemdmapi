from ..api import SimpleMDMConnector
from ..typehints import OptionalString, OptionalDict, UnionIntString
from typing import Any


class Apps(SimpleMDMConnector):
    """Apps.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#apps
    """
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, app_store_id: OptionalString = None, bundle_id: OptionalString = None,
               binary: OptionalString = None, name: OptionalString = None) -> Any:
        """Upload/create an app. Can only supply one of 'app_store_id', 'bundle_id', or 'binary'.

        The 'name' param can only be used with the 'binary' param.

        :param app_store_id: the Apple Store id value for the app to add
        :param bundle_id: the bundle id value for the app to add
        :param binary: file path (as a string) to the app to upload, can only upload '.pkg' files
        :param name: the name to use when uploading a binary"""
        files = {"binary": binary} if binary else dict()
        params = self.kwargs2params(self.create, locals(), ["files"])
        return self.post(params=params, files=files, upload_key="binary").json()  # Return created app object

    def delete_app(self, app_id: UnionIntString) -> Any:
        """Delete an app.

        :param app_id: the id value"""
        return self.delete(url=f"{app_id}")  # Return 204 status

    def list_all(self) -> Any:
        """List all applications."""
        self.paginate()  # Return list of app objects

    def list_installs(self, app_id: UnionIntString) -> Any:
        """List all applications.

        :param app_id: the id value"""
        return self.paginate(url=f"{app_id}/installs")  # Return list of app install objects

    def retrieve(self, app_id: UnionIntString) -> Any:
        """Retrieve one application.

        :param app_id: the id value"""
        return self.get(url=f"{app_id}").json()  # Return app object

    def update(self, app_id: UnionIntString, binary: OptionalString = None,
               deploy_to: OptionalString = None, name: OptionalString = None) -> Any:
        """Update details about an app.

        :param app_id: the id value
        :param binary: file path (as a string) to the app to upload, can only upload '.pkg' files
        :param name: the name to use when uploading a binary"""
        files = {"binary": binary} if binary else dict()
        params = self.kwargs2params(self.update, locals(), ["app_id", "files"])
        return self.patch(url=f"{app_id}", params=params, files=files, upload_key="binary").json()  # Return app update object


class ManagedAppConfigs(SimpleMDMConnector):
    """Managed App Configs.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#managed-app-configs
    """
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_config(self, app_id: UnionIntString) -> Any:
        """Retrieve managed application configuration.

        :param app_id: the id value"""
        return self.get(url=f"{app_id}/managed_configs").json()  # Return app object

    def create(self, app_id: UnionIntString, key: str, value: OptionalString = None, value_type: OptionalString = None) -> Any:
        """Create a managed app config.

        :param key: the key name.
        :param value: default value the key will have
        :param value_type: the type the value is expected to be"""
        params = self.kwargs2params(self.create, locals(), ["app_id"])
        return self.post(url=f"{app_id}/managed_configs", params=params).json()  # Return created app object

    def delete_config(self, app_id: UnionIntString, config_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete a managed config for an app.

        :param app_id: the id value
        :praam config_id: the id value"""
        return self.delete(url=f"{app_id}/managed_configs/{config_id}")  # Return 204 status

    def push_updates(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Push a managed config for an app to all devices with that app. Only required for changes
        made to a managed app config via API.

        :param app_id: the id value"""
        return self.post(url=f"{app_id}/managed_configs/push").json()  # Return app update object
