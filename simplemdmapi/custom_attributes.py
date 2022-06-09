from .connector import SimpleMDMConnector
from .typehints import OptionalString, UnionIntString
from typing import Any


class CustomAttributes(SimpleMDMConnector):
    """Simple MDM Custom Attributes.
    https://simplemdm.com/docs/api/#custom-attributes"""
    def __init__(self, endpoint: str = "custom_attributes") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, name: str, default_value: OptionalString = None) -> Any:
        """Create an custom attribute.
        :param name: name of the custom attribute
        :param default_value: the default value of the custom attribute"""
        params = self.kwargs2params(self.create, locals(), ["params", "name", "default_value"])
        return self.post(params=params).json()  # Return custom attribute object

    def delete_attribute(self, attr_id: UnionIntString) -> Any:
        """Delete an custom attribute.
        :param attr_id: the id value"""
        return self.delete(url=f"{attr_id}").json()  # Return ??

    def list_all(self) -> Any:
        """List all custom attributes."""
        return self.paginate()  # Return list of custom attribute objects

    def retrieve(self, attr_id: UnionIntString) -> Any:
        """Retrieve one application.
        :param attr_id: the id value"""
        return self.get(url=f"{attr_id}").json()  # Return custom attribute object

    def update(self, attr_id: UnionIntString, default_value: OptionalString = None) -> Any:
        """Update details about an custom attribute.
        :param attr_id: the id value
        :param default_value: the updated default value"""
        params = self.kwargs2params(self.update, locals(), ["params", "attr_id", "default_value"])
        return self.patch(url=f"{attr_id}", params=params).json()  # Return ??
