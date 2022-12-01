from typing import Optional
from requests.models import Response
from ..connector import SimpleMDMConnector


class CustomAttributes(SimpleMDMConnector):
    """Custom Attributes.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#custom-attributes
    """
    def __init__(self, endpoint: str = "custom_attributes") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, name: str, default_value: Optional[str] = None, **kwargs) -> Response:
        """Create an custom attribute.

        :param name: name of the custom attribute
        :param default_value: the default value of the custom attribute"""
        params = self._k2p(self.create, vals=locals(), ignored_locals=["name", "default_value"])
        return self.post(params=params, **kwargs)

    def delete_attribute(self, attr_id: int | str, **kwargs) -> Response:
        """Delete an custom attribute.

        :param attr_id: the id value"""
        return self.delete(url=f"{attr_id}", **kwargs)

    def list_all(self, **kwargs) -> Response:
        """List all custom attributes."""
        return self.paginate(**kwargs)

    def retrieve(self, attr_id: int | str, **kwargs) -> Response:
        """Retrieve one application.

        :param attr_id: the id value"""
        return self.get(url=f"{attr_id}", **kwargs)  # Return custom attribute object

    def update(self, attr_id: int | str, default_value: Optional[str] = None, **kwargs) -> Response:
        """Update details about an custom attribute.

        :param attr_id: the id value
        :param default_value: the updated default value"""
        params = self._k2p(self.update, vals=locals(), ignored_locals=["attr_id", "default_value"])
        return self.patch(url=f"{attr_id}", params=params, **kwargs)
