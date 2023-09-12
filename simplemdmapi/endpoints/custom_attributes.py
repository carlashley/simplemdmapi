from requests.models import Response
from typing import Generator, Optional

from ..connector import SimpleMDMConnector
from .._decorators import paginate, param_kwargs
from .._validators import all_params, any_params, validate_param_opts

_param_kwargs = {
    "list_all": [
        "starting_after",
        "limit",
    ],
    "create": ["name", "default_value"],
    "update": ["default_value"],
}

_param_opts_validation = {
    "update_os": [
        ("os_update_mode", ["smart_update", "download_only", "notify_only", "install_asap", "force_update"]),
        ("version_type", ["latest_minor_version", "latest_major_version"]),
    ]
}


class CustomAttributes(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#custom-attributes"""
    # getting custom attributes for:
    # - devices: use the 'devices.Devices' class
    # - device groups: use the 'device_groups.DeviceGroups' class

    def __init__(self, endpoint: str = "custom_attributes", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @param_kwargs(_param_kwargs["list_all"])
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all custom attributes.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: custom attribute id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    def retrieve(self, attr_id: str, **kwargs) -> Response:
        """Retrieve one device.
        :param attr_id: id of the custom attribute"""
        return self.get(f"{attr_id}", **kwargs)

    @all_params(["name"])
    @any_params(_param_kwargs["create"])
    @param_kwargs(_param_kwargs["create"])
    def create(self, **kwargs) -> Response:
        """Create a custom attribute.
        :param name: custom attribute name
        :param default_value: optional default value the custom attribute will pre-fill if no value provided"""
        return self.post(**kwargs)

    @param_kwargs(_param_kwargs["update"])
    def update_attribute(self, attr_id: str, **kwargs) -> Response:
        """Update attribute.
        :param attr_id: id of the custom attribute to update
        :param default_value: optional default value the custom attribute will pre-fill if no value provided"""
        return self.patch(f"{attr_id}", **kwargs)

    def delete_attribute(self, attr_id: str, **kwargs) -> Response:
        """Delete attribute.
        :param attr_id: id of the custom attribute to delete"""
        return self.delete(f"{attr_id}", **kwargs)
