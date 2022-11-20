from ..connector import SimpleMDMConnector
from typing import Any, Optional


class CustomAttributes(SimpleMDMConnector):
    """Custom Attributes.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#custom-attributes
    """
    def __init__(self, endpoint: str = "custom_attributes") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, name: str, default_value: Optional[str] = None, **kwargs) -> Any:
        """Create an custom attribute.

        :param name: name of the custom attribute
        :param default_value: the default value of the custom attribute"""
        params = self._k2p(self.create, locals(), ["name", "default_value"])
        return self.post(params=params, **kwargs).json()  # Return custom attribute object

    def delete_attribute(self, attr_id: int | str, **kwargs) -> Any:
        """Delete an custom attribute.

        :param attr_id: the id value"""
        return self.delete(url=f"{attr_id}", **kwargs).json()  # Return ??

    def list_all(self, **kwargs) -> Any:
        """List all custom attributes."""
        return self.paginate(**kwargs)  # Return list of custom attribute objects

    def retrieve(self, attr_id: int | str, **kwargs) -> Any:
        """Retrieve one application.

        :param attr_id: the id value"""
        return self.get(url=f"{attr_id}", **kwargs).json()  # Return custom attribute object

    def update(self, attr_id: int | str, default_value: Optional[str] = None, **kwargs) -> Any:
        """Update details about an custom attribute.

        :param attr_id: the id value
        :param default_value: the updated default value"""
        params = self._k2p(self.update, locals(), ["attr_id", "default_value"])
        return self.patch(url=f"{attr_id}", params=params, **kwargs).json()  # Return ??
