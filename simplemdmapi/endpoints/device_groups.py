from requests.models import Response
from typing import Generator

from ..connector import SimpleMDMConnector
from .._decorators import paginate, api_path_suffix


class DeviceGroups(SimpleMDMConnector):
    def __init__(self, endpoint: str = "device_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    @paginate
    def list_all(self, limit: int = 100, starting_after: int = 0, **kwargs) -> Generator[dict, None, None]:
        """List all group groups.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: group id to start pagination after; default is 0 for first device"""
        params = {"limit": limit, "starting_after": starting_after}
        return self.get(params=params, **kwargs)

    def retrieve(self, group_id: str, **kwargs) -> Response:
        """Retrieve one device.
        :param group_id: id of the group to retrieve"""
        return self.get(group_id, **kwargs)

    @api_path_suffix("clone")
    def clone(self, group_id: str, **kwargs) -> Response:
        """Clone a group group.
        :param group_id: id of the group being cloned"""
        return self.post(group_id, **kwargs)

    @api_path_suffix("devices", ["device_id"])
    def assign_device(self, group_id: str, device_id: str, **kwargs) -> Response:
        """Assigns a device to a group.
        :param group_id: group id the device is to be assigned to
        :param device_id: the device id to assign to the group"""
        return self.post(group_id, **kwargs)

    @api_path_suffix("custom_attribute_values")
    def get_group_attributes(self, group_id: str, **kwargs) -> Response:
        """Retrieve custom attribute values for a device group.
        :param group_id: id of the group to retrieve"""
        return self.get(group_id, **kwargs)

    @api_path_suffix("custom_attribute_values", ["attr_name"])
    def set_group_attribute(self, group_id: str, attr_name: str, attr_value: str, **kwargs) -> Response:
        """Set a custom attribute for a device group.
        :param group_id: id of the group to retrieve
        :param attr_name: name of the attribute being created
        :param attr_value: value of the attribute"""
        params = {"value": attr_value}
        return self.put(group_id, params=params, **kwargs)
