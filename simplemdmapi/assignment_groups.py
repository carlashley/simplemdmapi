from .connector import SimpleMDMConnector
from .typehints import OptionalDict, UnionIntString
from typing import Any


class AssignmentGroups(SimpleMDMConnector):
    """Simple MDM Assignment Groups.
    https://simplemdm.com/docs/api/#assignment-groups"""
    def __init__(self, endpoint: str = "assignment_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_app(self, grp_id: UnionIntString, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Assign an application to an assignment group.
        :param grp_id: the id value.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/apps/{app_id}"

        return self.post(url=url, params=params, **kwargs)  # Return 204 status

    def unassign_app(self, grp_id: UnionIntString, app_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Unassign an application from an assignment group.
        :param grp_id: the id value.
        :param app_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/apps/{app_id}"

        return self.delete(url=url, params=params, **kwargs)  # Return 204 status

    def assign_device_group(self, grp_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Assign a device group to an assignment group.
        :param grp_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/device_groups/{device_grp_id}"

        return self.post(url=url, params=params, **kwargs)  # Return 204 status

    def unassign_device_group(self, grp_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Unassign a device group from an assignment group.
        :param grp_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/device_groups/{device_grp_id}"

        return self.delete(url=url, params=params, **kwargs)  # Return 204 status

    def assign_device(self, grp_id: UnionIntString, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Assign a device to an assignment group.
        :param grp_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/devices/{device_id}"

        return self.post(url=url, params=params, **kwargs)  # Return 204 status

    def unassign_device(self, grp_id: UnionIntString, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Unassign a device from an assignment group.
        :param grp_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/devices/{device_id}"

        return self.delete(url=url, params=params, **kwargs)  # Return 204 status

    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Create an assignment group.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["auto_deploy", "name"]
        kwargs["required_params"] = ["name"]

        return self.post(params=params, **kwargs)  # Return created assignment group object

    def delete_group(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{grp_id}", params=params, **kwargs)  # Return 204 status

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all assignment groups.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Return list of assignment group objects

    def retrieve(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve one application.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{grp_id}", params=params, **kwargs).json()  # Return assignment group object

    def update(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["auto_deploy", "name"]
        kwargs["required_params"] = ["name"]

        return self.patch(url=f"{grp_id}", params=params, **kwargs)  # Return 204 status

    def push_apps(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Push applications to an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/push_apps"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def update_apps(self, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Push application updates to an assignment group.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{grp_id}/update_apps"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status
