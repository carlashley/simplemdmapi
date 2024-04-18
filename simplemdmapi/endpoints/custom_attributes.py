from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate


class CustomAttributes(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#custom-attributes"""

    # getting custom attributes for:
    # - devices: use the 'devices.Devices' class
    # - device groups: use the 'device_groups.DeviceGroups' class

    def __init__(
        self, endpoint: str = "custom_attributes", dry_run: bool = False, tkn: Optional[str | Path] = None
    ) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
            "create": {
                "all_params": ["default_value", "name"],
                "req_params": ["name"],
            },
            "update": {
                "all_params": ["default_value"],
            },
        }

    @method_params
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all custom attributes.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: custom attribute id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    def retrieve(self, attr_id: str, **kwargs) -> Response:
        """Retrieve one device.
        :param attr_id: id of the custom attribute"""
        return self.get(attr_id, **kwargs)

    @method_params
    def create(self, **kwargs) -> Response:
        """Create a custom attribute.
        :param name: custom attribute name
        :param default_value: optional default value the custom attribute will pre-fill if no value provided"""
        return self.post(**kwargs)

    @method_params
    def update_attribute(self, attr_id: str, **kwargs) -> Response:
        """Update attribute.
        :param attr_id: id of the custom attribute to update
        :param default_value: optional default value the custom attribute will pre-fill if no value provided"""
        return self.patch(attr_id, **kwargs)

    def delete_attribute(self, attr_id: str, **kwargs) -> Response:
        """Delete attribute.
        :param attr_id: id of the custom attribute to delete"""
        return self.delete(attr_id, **kwargs)
