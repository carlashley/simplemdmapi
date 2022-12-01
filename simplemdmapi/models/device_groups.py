from requests.models import Response
from ..connector import SimpleMDMConnector


class DeviceGroups(SimpleMDMConnector):
    """Device Groups.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#device-groups
    """
    def __init__(self, endpoint: str = "device_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_device(self, grp_id: int | str, device_id: int | str, **kwargs) -> Response:
        """Assign a device to a device group.

        :param grp_id: the id value
        :param device_id: the id value"""
        return self.post(url=f"{grp_id}/devices/{device_id}", **kwargs)

    def clone(self, grp_id: int | str, **kwargs) -> Response:
        """Clone a device group.

        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/clone", **kwargs)

    def list_all(self, **kwargs) -> Response:
        """List all device groups."""
        return self.paginate(**kwargs)

    def retrieve(self, grp_id: int | str, **kwargs) -> Response:
        """Retrieve a device group.

        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}", **kwargs)

    def get_attributes(self, grp_id: int | str, **kwargs) -> Response:
        """Get custom attributes for a specific device group.

        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}/custom_attribute_values", **kwargs)

    def set_attribute(self, grp_id: int | str, attr_name: str, attr_value: str, **kwargs) -> Response:
        """Set custom attributes for a specific device group

        :param grp_id: the id value
        :param attr_name: the name of the custom attribute to set the attribute value of
        :param attr_value: the value to set"""
        params = self._k2p(self.set_attribute, vals=locals(), ignored_locals=["grp_id", "attr_name"])
        return self.put(url=f"{grp_id}/custom_attribute_values/{attr_name}", params=params, **kwargs)
