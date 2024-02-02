from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate, url_suffixes


class Apps(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#apps"""

    def __init__(self, endpoint: str = "apps", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
            "create": {
                "all_params": ["app_store_id", "binary", "bundle_id", "name"],
                "any_params": ["app_store_id", "bundle_id", "binary"],
                "inc_params": (
                    ["app_store_id", "bundle_id", "binary"],
                    ["app_store_id", "bundle_id", "name"],
                ),
                "file_param": "binary",
            },
            "update": {
                "all_params": ["binary", "deploy_to", "name"],
                "any_params": ["binary", "deploy_to", "name"],
                "file_param": "binary",
                "validate": {
                    "deploy_to": ["all", "none", "outdated"],
                },
            },
        }

    @method_params
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all apps."""
        return self.get(**kwargs)

    @method_params
    def retrieve(self, app_id: str, **kwargs) -> Response:
        """Retrieve one app.
        :param app_id: id of the app"""
        return self.get(app_id, **kwargs)

    @method_params
    def create(self, **kwargs) -> Response:
        """Add's an app to SimpleMDM from either App Store, or via upload.
        :param app_store_id: Apple App Store ID of the app to add; for example: '1090161858'
        :param binary: string representation of the file path to a macOS '.pkg' file to upload; this cannot be used
                       with 'app_store_id' and/or 'bundle_id'
        :param bundle_id: bundle id of the Apple App Store app to add; for example: 'foo.example.org'
        :param name: optional name to use as the display name, SimpleMDM will automatically determine the name based
                     on the binary if this param is not provided, can be used with 'binary'"""
        return self.post(**kwargs)

    @method_params
    def update(self, app_id: str, **kwargs) -> Response:
        """Update name/app name for a app.
        :param app_id: id of the app
        :param binary: string representation of the file path to a macOS '.pkg' file to upload
        :param deploy_to: deploy the app to associated devices immediately after upload and processing is completed;
                          when set to 'outdated' and a newer version of an app is uploaded, teh app will be deployed
                          to devices that have an outdated version of the app, when set to 'all', app is deployed to
                          all devices regardless if the app is already installed, when set to 'non' the app will not
                          be deployed; default is 'none'.
        :param name: app name that appears within SimpleMDM (this is not the app hostname)"""
        return self.patch(app_id, **kwargs)

    def remove(self, app_id: str, **kwargs) -> Response:
        """Delete an app.
        :param app_id: id of the app"""
        return self.delete(app_id, **kwargs)

    @url_suffixes("installs")
    @paginate
    def list_installs(self, app_id: str, **kwargs) -> Generator[dict, None, None]:
        """List devices an application is installed on
        :param app_id: id of the app"""
        return self.get(app_id, **kwargs)


class ManagedAppConfigs(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#managed-app-configs"""

    def __init__(self, endpoint: str = "apps", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "create": {
                "all_params": ["key", "value", "value_type"],
                "req_params": ["key"],
                "validate": {
                    "value_type": [
                        "boolean",
                        "date",
                        "float",
                        "float array",
                        "integer",
                        "integer array",
                        "string",
                        "string array",
                    ],
                },
            },
            "delete": {
                "all_params": ["config_id"],
            },
        }

    @url_suffixes("managed_configs")
    def get_config(self, app_id: str, **kwargs) -> Generator[dict, None, None]:
        """List all managed app configs.
        :param app_id: id of the app"""
        return self.get(app_id, **kwargs)

    @method_params
    @url_suffixes("managed_configs")
    def create(self, app_id: str, **kwargs) -> Response:
        """Create a managed app config.
        :param app_id: id of the app
        :param key: required string, this is the key that will be added to the managed config
        :param value: the value that the key will have
        :param value_type: specify the value type, valid options are: 'boolean' (0 or 1), 'date' (timestamp
                           format with timezone, for example: '2023-09-31T09:30:00-10:00'), 'float' (0.123),
                           'float array' (comma separated, 0.1,1.1,2.9), 'integer' (32), 'integer array' (comma
                           separated, 1,2,3,4), 'string', 'string array' (quoted & comma separated, "hello","world")"""
        return self.post(app_id, **kwargs)

    @method_params
    @url_suffixes("managed_configs", ["config_id"])
    def delete_config(self, app_id: str, **kwargs) -> Generator[dict, None, None]:
        """Delete managed app config.
        :param app_id: id of the app
        :param config_id: id of the managed config"""
        return self.delete(app_id, **kwargs)

    @url_suffixes("managed_configs/push")
    def push_update(self, app_id: str, **kwargs) -> Generator[dict, None, None]:
        """Push an update to managed app config for all devices (only required if making a change through the API).
        :param app_id: id of the app"""
        return self.post(app_id, **kwargs)


class InstalledApps(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#installed-app-configs"""

    def __init__(
        self, endpoint: str = "installed_apps", dry_run: bool = False, tkn: Optional[str | Path] = None
    ) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

    def retrieve(self, app_id: str, **kwargs) -> Response:
        """Retrieve details of an installed app.
        :param app_id: id of the app"""
        return self.get(app_id, **kwargs)

    @url_suffixes("request_management")
    def request_management(self, app_id: str, **kwargs) -> Response:
        """Request management of an unmanaged app on a device; iOS, tvOS, and macOS (11+).
        :param app_id: id of the app"""
        return self.post(app_id, **kwargs)

    @url_suffixes("update")
    def install_update(self, app_id: str, **kwargs) -> Response:
        """Request the device update an app.
        :param app_id: id of the app"""
        return self.post(app_id, **kwargs)

    def uninstall(self, app_id: str, **kwargs) -> Response:
        """Request a device to uninstall an app.
        :param app_id: id of the app"""
        return self.delete(app_id, **kwargs)
