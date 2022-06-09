from .connector import SimpleMDMConnector
from .typehints import UnionIntString
from typing import Any


class DeviceGroups(SimpleMDMConnector):
    """Simple MDM Device Groups.
    https://simplemdm.com/docs/api/#device-groups"""
    def __init__(self, endpoint: str = "device_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_device(self, grp_id: UnionIntString, device_id: UnionIntString) -> Any:
        """Assign a device to a device group.
        :param grp_id: the id value
        :param device_id: the id value"""
        return self.post(url=f"{grp_id}/devices/{device_id}")  # Return 202 on success

    def clone(self, grp_id: UnionIntString) -> Any:
        """Clone a device group.
        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/clone").json()  # Return json content of new group

    def list_all(self) -> Any:
        """List all device groups."""
        return self.paginate()  # Return list of group objects

    def retrieve(self, grp_id: UnionIntString) -> Any:
        """Retrieve a device group.
        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}")  # Return single group object

    def get_attributes(self, grp_id: UnionIntString) -> Any:
        """Get custom attributes for a specific device group.
        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}/custom_attribute_values").json()  # Return json content of attributes

    def set_attribute(self, grp_id: UnionIntString, attr_name: str, attr_value: str) -> Any:
        """Set custom attributes for a specific device group
        :param grp_id: the id value
        :param attr_name: the name of the custom attribute to set the attribute value of
        :param attr_value: the value to set"""
        params = self.kwargs2params(self.set_attribute, locals(), ["params", "grp_id", "attr_name"])
        return self.put(url=f"{grp_id}/custom_attribute_values/{attr_name}", params=params).json()  # Return json content of updated value
