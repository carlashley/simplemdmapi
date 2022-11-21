from ..connector import SimpleMDMConnector
from typing import Any


class DeviceGroups(SimpleMDMConnector):
    """Device Groups.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#device-groups
    """
    def __init__(self, endpoint: str = "device_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_device(self, grp_id: int | str, device_id: int | str, **kwargs) -> Any:
        """Assign a device to a device group.

        :param grp_id: the id value
        :param device_id: the id value"""
        return self.post(url=f"{grp_id}/devices/{device_id}", **kwargs)  # Return 202 on success

    def clone(self, grp_id: int | str, **kwargs) -> Any:
        """Clone a device group.

        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/clone", **kwargs).json()  # Return json content of new group

    def list_all(self, **kwargs) -> Any:
        """List all device groups."""
        return self.paginate(**kwargs)  # Return list of group objects

    def retrieve(self, grp_id: int | str, **kwargs) -> Any:
        """Retrieve a device group.

        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}", **kwargs)  # Return single group object

    def get_attributes(self, grp_id: int | str, **kwargs) -> Any:
        """Get custom attributes for a specific device group.

        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}/custom_attribute_values", **kwargs).json()  # Return json content of attributes

    def set_attribute(self, grp_id: int | str, attr_name: str, attr_value: str, **kwargs) -> Any:
        """Set custom attributes for a specific device group

        :param grp_id: the id value
        :param attr_name: the name of the custom attribute to set the attribute value of
        :param attr_value: the value to set"""
        params = self._k2p(self.set_attribute, vals=locals(), ignored_locals=["grp_id", "attr_name"])
        # Return JSON content of the updated value
        return self.put(url=f"{grp_id}/custom_attribute_values/{attr_name}", params=params, **kwargs).json()
