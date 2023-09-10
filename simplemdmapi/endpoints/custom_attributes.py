from requests.models import Response
from typing import Generator, Optional

from ..connector import SimpleMDMConnector
from .._decorators import paginate


class CustomAttributes(SimpleMDMConnector):
    def __init__(self, endpoint: str = "custom_attributes") -> None:
        self.endpoint = endpoint
        super().__init__()

    @paginate
    def list_all(self, limit: int = 100, starting_after: int = 0, **kwargs) -> Generator[dict, None, None]:
        """List all custom attributes.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: custom attribute id to start pagination after; default is 0 for first device"""
        params = {"limit": limit, "starting_after": starting_after}
        return self.get(params=params, **kwargs)

    def retrieve(self, attr_id: str, inc_secret_attrs: bool = True, **kwargs) -> Response:
        """Retrieve one device.
        :param attr_id: id of the custom attribute to retrieve"""
        return self.get(attr_id, **kwargs)

    def create(self, name: str, default_value: Optional[str] = None, **kwargs) -> Response:
        """Create a custom attribute.
        :param name: custom attribute name
        :param default_value: optional default value the custom attribute will pre-fill if no value provided"""
        params = {"name": name}

        if default_value:
            params["default_value"] = default_value

        return self.post(params=params, **kwargs)

    def update_attribute(self, attr_id: str, default_value: Optional[str] = None, **kwargs) -> Response:
        """Update attribute.
        :param attr_id: id of the custom attribute to update
        :param default_value: optional default value the custom attribute will pre-fill if no value provided"""
        params = {}

        if default_value:
            params["default_value"] = default_value

        return self.patch(attr_id, params=params, **kwargs)

    def remove_attribute(self, attr_id: str) -> Response:
        """Remove attribute.
        :param attr_id: id of the custom attribute to delete"""
        return self.delete(attr_id)
