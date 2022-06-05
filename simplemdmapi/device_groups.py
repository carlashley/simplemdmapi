from .connector import SimpleMDMConnector
from .typehints import (OptionalDict,
                        UnionIntString)
from typing import Any


class DeviceGroups(SimpleMDMConnector):
    """Simple MDM Device Groups"""
    def __init__(self, endpoint: str = "device_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def get_attributes(self, device_grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Get custom attributes for a specific device group.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_grp_id}/custom_attribute_valuess"

        return SimpleMDMConnector.get(url=url)(lambda _: (params, kwargs))(self).json()

    def set_attribute(self, device_grp_id: UnionIntString, attr_name: str, params: OptionalDict, **kwargs) -> Any:
        """Set custom attributes for a specific device group
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        reqrd_params = ["value"]
        self.validate_params(params, reqrd_params)
        self.required_params(params, reqrd_params)

        url = f"{device_grp_id}/custom_attribute_values/{attr_name}"
        return SimpleMDMConnector.put(url=url)(lambda _: (params, kwargs))(self).json()
    # @SimpleMDMConnector.post()
    # def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
    #     """Create an custom attribute.
    #     :param params: specific parameters to provide to the API query.
    #     :param kwargs: specific parameters to provide to the underlying requests function."""
    #     valid_params = ["default_value", "name"]
    #     reqrd_params = ["name"]
    #     self.required_params(params, reqrd_params)
    #     self.validate_params(params, valid_params)

    #     return params, kwargs

    # def delete_attribute(self, device_grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
    #     """Delete an custom attribute.
    #     :param device_grp_id: the id value.
    #     :param params: specific parameters to provide to the API query.
    #     :param kwargs: specific parameters to provide to the underlying requests function."""
    #     SimpleMDMConnector.delete(url=device_grp_id)(lambda _: (params, kwargs))(self)

    # @SimpleMDMConnector.paginate()
    # def list_all(self, params: OptionalDict, **kwargs) -> Any:
    #     """List all custom attributes.
    #     :param params: specific parameters to provide to the API query.
    #     :param kwargs: specific parameters to provide to the underlying requests function."""
    #     return params, kwargs

    # def retrieve(self, device_grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
    #     """Retrieve one application.
    #     :param device_grp_id: the id value.
    #     :param params: specific parameters to provide to the API query.
    #     :param kwargs: specific parameters to provide to the underlying requests function."""
    #     return SimpleMDMConnector.get(url=device_grp_id)(lambda _: (params, kwargs))(self).json()

    # def update(self, device_grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
    #     """Update details about an custom attribute.
    #     :param device_grp_id: the id value.
    #     :param params: specific parameters to provide to the API query.
    #     :param kwargs: specific parameters to provide to the underlying requests function."""
    #     valid_params = ["default_value"]

    #     if params:
    #         self.validate_params(params, valid_params)

    #     return SimpleMDMConnector.patch(url=device_grp_id)(lambda _: (params, kwargs))(self).json()
