from .connector import SimpleMDMConnector
from .typehints import OptionalDict, UnionIntString
from typing import Any


class DeviceGroups(SimpleMDMConnector):
    """Simple MDM Device Groups.
    https://simplemdm.com/docs/api/#device-groups"""
    def __init__(self, endpoint: str = "device_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_device(self, grp_id: UnionIntString, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Assign a device to a device group.
        :param grp_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/devices/{device_id}"

        return self.post(url=url, params=params, **kwargs)  # Return 202 on success

    def clone(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Clone a device group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/clone"

        return self.post(url=url, params=params, **kwargs).json()  # Return json content of new group

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all device groups.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Return list of group objects

    def retrieve(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve a device group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{grp_id}", params=params, **kwargs)  # Return single group object

    def get_attributes(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Get custom attributes for a specific device group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/custom_attribute_values"

        return self.get(url=url, params=params, **kwargs).json()  # Return json content of attributes

    def set_attribute(self, grp_id: UnionIntString, attr_name: str, params: OptionalDict = dict(), **kwargs) -> Any:
        """Set custom attributes for a specific device group
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["required_params"] = ["value"]
        kwargs["validate_params"] = ["value"]

        url = f"{grp_id}/custom_attribute_values/{attr_name}"
        return self.put(url=url, params=params, **kwargs).json()  # Return json content of updated value
