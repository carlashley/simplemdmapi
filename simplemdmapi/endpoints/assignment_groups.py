from requests.models import Response
from typing import Generator

from ..connector import SimpleMDMConnector
from .._decorators import paginate, param_kwargs, url_suffixes
from .._validators import all_params, any_params, validate_param_opts

_param_kwargs = {
    "list_all": [
        "starting_after",
        "limit",
    ],
    "create": ["auto_deploy", "install_type", "name", "type"],
    "update": ["auto_deploy", "name"],
    "assign_app": ["app_id"],
    "assign_device_grp": ["device_group_id"],
    "assign_device": ["device_id"],
}

_param_opts_validation = {
    "create": [
        ("auto_deploy", [True, False])("install_type", ["managed", "self_serve"]),
        ("type", ["munki", "standard"]),
    ]
}


class AssignmentGroups(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#apps"""

    def __init__(self, endpoint: str = "assignment_groups", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """list all assignment groups.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: device id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    def retrieve(self, group_id: str, **kwargs) -> Response:
        """Retrieve one assignment group.
        :param device_id: id of the assignment group"""
        return self.get(f"{group_id}", **kwargs)

    @all_params(["name"])
    @any_params(["auto_deploy", "install_type", "type"])
    @param_kwargs(_param_kwargs["create"])
    @validate_param_opts(_param_opts_validation["create"])
    def create(self, **kwargs) -> Response:
        """Create an assignment group.
        :param name: required, string representation of the assignment group
        :param auto_deploy: optional, determines if the app is automatically pushed to devices when they join
                            related device groups; default is 'True'
        :param type: optional, use 'standard' (for MDM app/media deployment) or a 'munki' to indicate the group
                     is for Munki app deployments; default is 'standard'
        :param install_type: optional; only used for Munki assignment groups, use 'managed' for managed app install
                             or 'self_serve' for optional install; default is 'managed'"""
        return self.post(**kwargs)

    @any_params(_param_kwargs["update"])
    @param_kwargs(_param_kwargs["update"])
    def update(self, group_id: str, **kwargs) -> Response:
        """Update an assignment group.
        :param group_id: id of the assignment group
        :param name: name of the assignment group
        :param auto_deploy: optional, determines if the app is automatically pushed to devices when they join
                            related device groups; default is 'True'"""
        return self.patch(f"{group_id}", **kwargs)

    def delete(self, group_id: str, **kwargs) -> Response:
        """Delete an assignment group.
        :param group_id: id of the assignment group"""
        return self.delete(f"{group_id}", **kwargs)

    @all_params(_param_kwargs["assign_app"])
    @url_suffixes("apps", ["app_id"])
    def assign_app(self, group_id: str, **kwargs) -> Response:
        """Assign an app to an assignment group.
        :param group_id: id of the assignment group
        :param app_id: id of the application"""
        return self.post(f"{group_id}")

    @all_params(_param_kwargs["assign_app"])
    @url_suffixes("apps", ["app_id"])
    def unassign_app(self, group_id: str, **kwargs) -> Response:
        """Unassign an app from an assignment group.
        :param group_id: id of the assignment group
        :param app_id: id of the application"""
        return self.delete(f"{group_id}", **kwargs)

    @all_params(_param_kwargs["assign_device_grp"])
    @url_suffixes("device_groups", ["device_group_id"])
    def assign_device_group(self, group_id: str, **kwargs) -> Response:
        """Assign a device group to an assignment group.
        :param group_id: id of the assignment group
        :param device_group_id: id of the device group"""
        return self.post(f"{group_id}")

    @all_params(_param_kwargs["assign_device_grp"])
    @url_suffixes("device_groups", ["device_group_id"])
    def unassign_device_group(self, group_id: str, **kwargs) -> Response:
        """Unassign a device group from an assignment group.
        :param group_id: id of the assignment group
        :param device_group_id: id of the device group"""
        return self.delete(f"{group_id}", **kwargs)

    @all_params(_param_kwargs["assign_device"])
    @url_suffixes("devices", ["device_id"])
    def assign_device(self, group_id: str, **kwargs) -> Response:
        """Assign a device to an assignment group.
        :param group_id: id of the assignment group
        :param device_group_id: id of the device group"""
        return self.post(f"{group_id}")

    @all_params(_param_kwargs["assign_device"])
    @url_suffixes("devices", ["device_id"])
    def unassign_device(self, group_id: str, **kwargs) -> Response:
        """Unassign a device from an assignment group.
        :param group_id: id of the assignment group
        :param device_group_id: id of the device group"""
        return self.delete(f"{group_id}", **kwargs)

    @url_suffixes("push_apps")
    def push_apps(self, group_id: str, **kwargs) -> Response:
        """Push apps to devices associated with the assignment group.
        :param group_id: id of the assignment group"""
        return self.post(f"{group_id}")

    @url_suffixes("update_apps")
    def update_apps(self, group_id: str, **kwargs) -> Response:
        """Update apps on devices associated with the assignment group.
        :param group_id: id of the assignment group"""
        return self.delete(f"{group_id}", **kwargs)
