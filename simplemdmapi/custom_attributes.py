from .connector import SimpleMDMConnector
from .typehints import OptionalDict, UnionIntString
from typing import Any


class CustomAttributes(SimpleMDMConnector):
    """Simple MDM Custom Attributes.
    https://simplemdm.com/docs/api/#custom-attributes"""
    def __init__(self, endpoint: str = "custom_attributes") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Create an custom attribute.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["required_params"] = ["name"]
        kwargs["validate_params"] = ["default_value", "name"]

        return self.post(params=params, **kwargs).json()  # Return custom attribute object

    def delete_attribute(self, attr_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an custom attribute.
        :param attr_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{attr_id}", params=params, **kwargs).json()  # Return ??

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all custom attributes.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Return list of custom attribute objects

    def retrieve(self, attr_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve one application.
        :param attr_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{attr_id}", params=params, **kwargs).json()  # Return custom attribute object

    def update(self, attr_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about an custom attribute.
        :param attr_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["default_value"]

        return self.patch(url=f"{attr_id}", params=params, **kwargs).json()  # Return ??
