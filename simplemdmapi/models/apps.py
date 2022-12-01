from requests.models import Response
from ..connector import SimpleMDMConnector


class AssignmentGroups(SimpleMDMConnector):
    """Assignment Groups.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#assignment-groups
    """
    def __init__(self, endpoint: str = "assignment_groups") -> None:
        self.endpoint = endpoint
        super().__init__()

    def assign_app(self, grp_id: int | str, app_id: int | str, **kwargs) -> Response:
        """Assign an application to an assignment group.

        :param grp_id: the id value
        :param app_id: the id value"""
        return self.post(url=f"{grp_id}/apps/{app_id}", **kwargs)  # Return 204 status

    def unassign_app(self, grp_id: int | str, app_id: int | str, **kwargs) -> Response:
        """Unassign an application from an assignment group.

        :param grp_id: the id value
        :param app_id: the id value"""
        return self.delete(url=f"{grp_id}/apps/{app_id}", **kwargs)  # Return 204 status

    def assign_device_group(self, grp_id: int | str, device_grp_id: int | str, **kwargs) -> Response:
        """Assign a device group to an assignment group.

        :param grp_id: the id value
        :param device_grp_id: the id value"""
        return self.post(url=f"{grp_id}/device_groups/{device_grp_id}", **kwargs)  # Return 204 status

    def unassign_device_group(self, grp_id: int | str, device_grp_id: int | str, **kwargs) -> Response:
        """Unassign a device group from an assignment group.

        :param grp_id: the id value
        :param device_grp_id: the id value"""
        return self.delete(url=f"{grp_id}/device_groups/{device_grp_id}", **kwargs)  # Return 204 status

    def assign_device(self, grp_id: int | str, device_id: int | str, **kwargs) -> Response:
        """Assign a device to an assignment group.

        :param grp_id: the id value
        :param device_id: the id value"""
        return self.post(url=f"{grp_id}/devices/{device_id}", **kwargs)  # Return 204 status

    def unassign_device(self, grp_id: int | str, device_id: int | str, **kwargs) -> Response:
        """Unassign a device from an assignment group.

        :param grp_id: the id value
        :param device_id: the id value"""
        return self.delete(url=f"{grp_id}/devices/{device_id}", **kwargs)  # Return 204 status

    def create(self, name: str, auto_deploy: bool = True, **kwargs) -> Response:
        """Create an assignment group.

        :param name: assignment group name
        :param auto_deploy: whether apps should be automatically pushed when devices join
                            this assignment group, default is True."""
        params = self._k2p(self.create, vals=locals(), ignored_locals=["name", "auto_deploy"])
        return self.post(params=params, **kwargs)  # Return created assignment group object

    def delete_group(self, grp_id: int | str, **kwargs) -> Response:
        """Delete an assignment group.

        :param grp_id: the id value"""
        return self.delete(url=f"{grp_id}", **kwargs)  # Return 204 status

    def list_all(self, **kwargs) -> Response:
        """List all assignment groups."""
        return self.paginate(**kwargs)

    def retrieve(self, grp_id: int | str, **kwargs) -> Response:
        """Retrieve one application.

        :param grp_id: the id value"""
        return self.get(url=f"{grp_id}", **kwargs)

    def update(self, grp_id: int | str, name: str, auto_deploy: bool = True, **kwargs) -> Response:
        """Update details about an assignment group.

        :param grp_id: the id value
        :param auto_deploy: whether apps should be automatically pushed when devices join
                            this assignment group, default is True."""
        params = self._k2p(self.update, vals=locals(), ignored_locals=["grp_id", "name", "auto_deploy"])
        return self.patch(url=f"{grp_id}", params=params, **kwargs)  # Return 204 status

    def push_apps(self, grp_id: int | str, **kwargs) -> Response:
        """Push applications to an assignment group.

        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/push_apps", **kwargs)  # Return 202 status

    def update_apps(self, grp_id: int | str, **kwargs) -> Response:
        """Push application updates to an assignment group.

        :param grp_id: the id value"""
        return self.post(url=f"{grp_id}/update_apps", **kwargs)  # Return 202 status
