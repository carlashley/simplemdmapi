from .connector import SimpleMDMConnector, APIParamException
from .typehints import (OptionalDict,
                        UnionIntString)
from typing import Any


class Apps(SimpleMDMConnector):
    """Simple MDM Apps"""
    def __init__(self, endpoint: str = "apps") -> None:
        self.endpoint = endpoint
        super().__init__()

    @SimpleMDMConnector.post(filename_key="binary")
    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Upload/create an app.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["app_store_id", "bundle_id", "binary", "name"]
        unique_params = ["app_store_id", "bundle_id", "binary"]
        name = params.get("name")
        binary = params.get("binary")

        if params:
            self.validate_params(params, valid_params)

        if name and not binary:
            raise APIParamException("Error: 'name' parameter cannot be used without 'binary' parameter.")

        if binary:
            self.validate_file_extensions(binary, [".pkg"])
            kwargs["files"] = {"binary": binary}
            del params["binary"]
        elif not binary:
            self.unique_params(params, unique_params)

        return params, kwargs

    def delete_app(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an app.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return SimpleMDMConnector.delete(url=app_id)(lambda _: (params, kwargs))(self)

    @SimpleMDMConnector.paginate()
    def list_all(self, params: OptionalDict, **kwargs) -> Any:
        """List all applications.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    def list_installs(self, app_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """List all applications.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{app_id}/installs"

        return SimpleMDMConnector.paginate(url=url)(lambda _: (params, kwargs))(self)

    def retrieve(self, app_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Retrieve one application.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return SimpleMDMConnector.get(url=app_id)(lambda _: (params, kwargs))(self).json()

    def update(self, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about an app.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["binary", "deploy_to", "name"]
        binary = params.get("binary")

        if params:
            self.validate_params(params, valid_params)

        if binary:
            self.validate_file_extensions(binary, [".pkg"])
            kwargs["files"] = {"binary": binary}
            del params["binary"]

        return SimpleMDMConnector.patch(url=app_id, filename_key="binary")(lambda _: (params, kwargs))(self).json()
