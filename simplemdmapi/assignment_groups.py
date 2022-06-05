from .connector import SimpleMDMConnector
from .typehints import (OptionalDict,
                        UnionIntString)
from typing import Any


class AssignmentGroups(SimpleMDMConnector):
    """Simple MDM Assignment Groups"""
    def __init__(self, endpoint: str = "assignment_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_app(self, grp_id: UnionIntString, app_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Assign an application to an assignment group.
        :param grp_id: the id value.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/apps/{app_id}"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()

    def unassign_app(self, grp_id: UnionIntString, app_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Unassign an application from an assignment group.
        :param grp_id: the id value.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/apps/{app_id}"

        return SimpleMDMConnector.delete(url=url)(lambda _: (params, kwargs))(self).json()

    def assign_device_group(self, grp_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Assign a device group to an assignment group.
        :param grp_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/device_groups/{device_grp_id}"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()

    def unassign_device_group(self, grp_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Unassign a device group from an assignment group.
        :param grp_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/device_groups/{device_grp_id}"

        return SimpleMDMConnector.delete(url=url)(lambda _: (params, kwargs))(self).json()

    def assign_device(self, grp_id: UnionIntString, device_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Assign a device to an assignment group.
        :param grp_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/devices/{device_id}"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()

    def unassign_device(self, grp_id: UnionIntString, device_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Unassign a device from an assignment group.
        :param grp_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/devices/{device_id}"

        return SimpleMDMConnector.delete(url=url)(lambda _: (params, kwargs))(self).json()

    @SimpleMDMConnector.post()
    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Create an assignment group.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["auto_deploy", "name"]
        reqrd_params = ["name"]
        self.required_params(params, reqrd_params)
        self.validate_params(params, valid_params)

        return params, kwargs

    def delete_group(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        SimpleMDMConnector.delete(url=grp_id)(lambda _: (params, kwargs))(self)

    @SimpleMDMConnector.paginate()
    def list_all(self, params: OptionalDict, **kwargs) -> Any:
        """List all assignment groups.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    def retrieve(self, grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Retrieve one application.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return SimpleMDMConnector.get(url=grp_id)(lambda _: (params, kwargs))(self).json()

    def update(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["auto_deploy", "name"]
        reqrd_params = ["name"]
        self.required_params(params, reqrd_params)
        self.validate_params(params, valid_params)

        return SimpleMDMConnector.patch(url=grp_id)(lambda _: (params, kwargs))(self).json()

    def push_apps(self, grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Push applications to an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/push_apps"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()

    def update_apps(self, grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Push application updates to an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/update_apps"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()
