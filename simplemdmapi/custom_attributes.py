from .connector import SimpleMDMConnector
from .typehints import (OptionalDict,
                        UnionIntString)
from typing import Any


class CustomAttributes(SimpleMDMConnector):
    """Simple MDM Custom Attributes"""
    def __init__(self, endpoint: str = "custom_attributes") -> None:
        self.endpoint = endpoint
        super().__init__()

    @SimpleMDMConnector.post()
    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Create an custom attribute.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["default_value", "name"]
        reqrd_params = ["name"]
        self.required_params(params, reqrd_params)
        self.validate_params(params, valid_params)

        return params, kwargs

    def delete_attribute(self, attr_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an custom attribute.
        :param attr_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        SimpleMDMConnector.delete(url=attr_id)(lambda _: (params, kwargs))(self)

    @SimpleMDMConnector.paginate()
    def list_all(self, params: OptionalDict, **kwargs) -> Any:
        """List all custom attributes.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    def retrieve(self, attr_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Retrieve one application.
        :param attr_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return SimpleMDMConnector.get(url=attr_id)(lambda _: (params, kwargs))(self).json()

    def update(self, attr_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about an custom attribute.
        :param attr_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["default_value"]

        if params:
            self.validate_params(params, valid_params)

        return SimpleMDMConnector.patch(url=attr_id)(lambda _: (params, kwargs))(self).json()
