from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate, url_suffixes


class DeviceGroups(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#device-groups"""

    def __init__(
        self, endpoint: str = "device_groups", dry_run: bool = False, tkn: Optional[str | Path] = None
    ) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
            "assign_device": {
                "all_params": ["device_id"],
                "req_params": ["device_id"],
            },
            "set_group_attribute": {
                "all_params": ["attr_name", "value"],
                "req_params": ["value"],
            },
        }

    @method_params
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all group groups.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: group id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    def retrieve(self, group_id: str, **kwargs) -> Response:
        """Retrieve one device group.
        :param group_id: id of the group to retrieve"""
        return self.get(group_id, **kwargs)

    @method_params
    @url_suffixes("devices", ["device_id"])
    def assign_device(self, group_id: str, device_id: str, **kwargs) -> Response:
        """Assigns a device to a group.
        :param group_id: group id the device is to be assigned to
        :param device_id: the device id to assign to the group"""
        return self.post(group_id, **kwargs)

    @url_suffixes("clone")
    def clone(self, group_id: str, **kwargs) -> Response:
        """Clone a group group.
        :param group_id: id of the group being cloned"""
        return self.post(group_id, **kwargs)

    @url_suffixes("custom_attribute_values")
    def get_group_attributes(self, group_id: str, **kwargs) -> Response:
        """Retrieve custom attribute values for a device group.
        :param group_id: id of the group to retrieve"""
        return self.get(group_id, **kwargs)

    @method_params
    @url_suffixes("custom_attribute_values", ["attr_name"])
    def set_group_attribute(self, group_id: str, attr_name: str, attr_value: str, **kwargs) -> Response:
        """Set a custom attribute for a device group.
        :param group_id: id of the group to retrieve
        :param attr_name: name of the attribute being created
        :param attr_value: value of the attribute"""
        return self.put(group_id, **kwargs)
