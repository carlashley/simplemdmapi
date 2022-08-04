from ..api import SimpleMDMConnector
from ..typehints import UnionIntString
from typing import Any


class AssignmentGroups(SimpleMDMConnector):
    """Assignment Groups.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#assignment-groups
    """
    def __init__(self, endpoint: str = "assignment_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_app(self, grp_id: UnionIntString, app_id: UnionIntString) -> Any:
        """Assign an application to an assignment group.

        :param grp_id: the id value
        :param app_id: the id value"""
        return self.post(url=f"{grp_id}/apps/{app_id}")  # Return 204 status

    def unassign_app(self, grp_id: UnionIntString, app_id: UnionIntString) -> Any:
        """Unassign an application from an assignment group.

        :param grp_id: the id value
        :param app_id: the id value"""
        return self.delete(url=f"{grp_id}/apps/{app_id}")  # Return 204 status

    def assign_device_group(self, grp_id: UnionIntString, device_grp_id: UnionIntString) -> Any:
        """Assign a device group to an assignment group.

        :param grp_id: the id value
        :param device_grp_id: the id value"""
        return self.post(url=f"{grp_id}/device_groups/{device_grp_id}")  # Return 204 status

    def unassign_device_group(self, grp_id: UnionIntString, device_grp_id: UnionIntString) -> Any:
        """Unassign a device group from an assignment group.

        :param grp_id: the id value
        :param device_grp_id: the id value"""
        return self.delete(url=f"{grp_id}/device_groups/{device_grp_id}")  # Return 204 status

    def assign_device(self, grp_id: UnionIntString, device_id: UnionIntString) -> Any:
        """Assign a device to an assignment group.

        :param grp_id: the id value
        :param device_id: the id value"""
        return self.post(url=f"{grp_id}/devices/{device_id}")  # Return 204 status

    def unassign_device(self, grp_id: UnionIntString, device_id: UnionIntString) -> Any:
        """Unassign a device from an assignment group.

        :param grp_id: the id value
        :param device_id: the id value"""
        return self.delete(url=f"{grp_id}/devices/{device_id}")  # Return 204 status

    def create(self, name: str, auto_deploy: bool = True) -> Any:
        """Create an assignment group.

        :param name: assignment group name
        :param auto_deploy: whether apps should be automatically pushed when devices join
                            this assignment group, default is True."""
        params = self.kwargs2params(self.create, locals(), ["name", "auto_deploy"])
        return self.post(params=params)  # Return created assignment group object

    def delete_group(self, grp_id: UnionIntString) -> Any:
        """Delete an assignment group.

        :param grp_id: the id value"""
        return self.delete(url=f"{grp_id}")  # Return 204 status

    def list_all(self) -> Any:
        """List all assignment groups."""
        return self.paginate()  # Return all assignment group objects

    def retrieve(self, grp_id: UnionIntString) -> Any:
        """Retrieve one application.

        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}").json()  # Return assignment group object

    def update(self, grp_id: UnionIntString, name: str, auto_deploy: bool = True) -> Any:
        """Update details about an assignment group.

        :param grp_id: the id value
        :param auto_deploy: whether apps should be automatically pushed when devices join
                            this assignment group, default is True."""
        params = self.kwargs2params(self.update, locals(), ["grp_id", "name", "auto_deploy"])
        return self.patch(url=f"{grp_id}", params=params)  # Return 204 status

    def push_apps(self, grp_id: UnionIntString) -> Any:
        """Push applications to an assignment group.

        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/push_apps")  # Return 202 status

    def update_apps(self, grp_id: UnionIntString) -> Any:
        """Push application updates to an assignment group.

        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/update_apps")  # Return 202 status
