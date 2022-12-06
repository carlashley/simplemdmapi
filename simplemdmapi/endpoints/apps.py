from typing import Optional
from requests.models import Response
from ..connector import SimpleMDMConnector


class Apps(SimpleMDMConnector):
    """Apps.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#apps
    """
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self,
               app_store_id: Optional[str] = None,
               bundle_id: Optional[str] = None,
               binary: Optional[str] = None,
               name: Optional[str] = None,
               **kwargs) -> Response:
        """Upload/create an app. Can only supply one of 'app_store_id', 'bundle_id', or 'binary'.

        The 'name' param can only be used with the 'binary' param.

        :param app_store_id: the Apple Store id value for the app to add
        :param bundle_id: the bundle id value for the app to add
        :param binary: file path (as a string) to the app to upload, can only upload '.pkg' files
        :param name: the name to use when uploading a binary"""
        files = {"binary": binary} if binary else dict()
        params = self._k2p(self.create, vals=locals(), ignored_locals=["files"])
        return self.post(params=params, files=files, upload_key="binary", **kwargs)

    def delete_app(self, app_id: int | str, **kwargs) -> Response:
        """Delete an app.

        :param app_id: the id value"""
        return self.delete(url=f"{app_id}", **kwargs)  # Return 204 status

    def list_all(self, **kwargs) -> Response:
        """List all applications."""
        self.paginate(**kwargs)  # Return list of app objects

    def list_installs(self, app_id: int | str, **kwargs) -> Response:
        """List all applications.

        :param app_id: the id value"""
        return self.paginate(url=f"{app_id}/installs", **kwargs)

    def retrieve(self, app_id: int | str, **kwargs) -> Response:
        """Retrieve one application.

        :param app_id: the id value"""
        return self.get(url=f"{app_id}", **kwargs)  # Return app object

    def update(self,
               app_id: int | str,
               binary: Optional[str] = None,
               deploy_to: Optional[str] = None,
               name: Optional[str] = None,
               **kwargs) -> Response:
        """Update details about an app.

        :param app_id: the id value
        :param binary: file path (as a string) to the app to upload, can only upload '.pkg' files
        :param name: the name to use when uploading a binary"""
        files = {"binary": binary} if binary else dict()
        params = self._k2p(self.update, vals=locals(), ignored_locals=["app_id", "files"])
        # Return app update object
        return self.patch(url=f"{app_id}", params=params, files=files, upload_key="binary", **kwargs)


class ManagedAppConfigs(SimpleMDMConnector):
    """Managed App Configs.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#managed-app-configs
    """
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_config(self, app_id: int | str, **kwargs) -> Response:
        """Retrieve managed application configuration.

        :param app_id: the id value"""
        return self.get(url=f"{app_id}/managed_configs", **kwargs)  # Return app object

    def create(self,
               app_id: int | str,
               key: str,
               value: str,
               value_type: str,
               **kwargs) -> Response:
        """Create a managed app config.

        :param key: the key name.
        :param value: default value the key will have
        :param value_type: the type the value is expected to be"""
        params = self._k2p(self.create, vals=locals(), ignored_locals=["app_id"])
        return self.post(url=f"{app_id}/managed_configs", params=params, **kwargs)

    def delete_config(self,
                      app_id: int | str,
                      config_id: int | str,
                      **kwargs) -> Response:
        """Delete a managed config for an app.

        :param app_id: the id value
        :param config_id: the id value"""
        return self.delete(url=f"{app_id}/managed_configs/{config_id}", **kwargs)

    def push_updates(self, app_id: int | str, **kwargs) -> Response:
        """Push a managed config for an app to all devices with that app. Only required for changes
        made to a managed app config via API.

        :param app_id: the id value"""
        return self.post(url=f"{app_id}/managed_configs/push", **kwargs)
