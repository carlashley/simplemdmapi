from requests.models import Response
from typing import Generator

from ..connector import SimpleMDMConnector
from .._decorators import paginate, param_kwargs, url_suffixes
from .._validators import all_params, any_params, validate_pin, validate_param_opts

_param_kwargs = {
    "list_all": [
        "search",
        "starting_after",
        "limit",
    ],
    "assign_to_device_group": ["device_group_id"],
    "assign_to_device": ["device_id"],
}

_param_opts_validation = {
    "update_os": [
        ("os_update_mode", ["smart_update", "download_only", "notify_only", "install_asap", "force_update"]),
        ("version_type", ["latest_minor_version", "latest_major_version"]),
    ]
}


class profiles(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#profiles"""

    def __init__(self, endpoint: str = "profiles", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @param_kwargs(_param_kwargs["list_all"])
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all profiles.
        :param search: optional, limit responses to profiles with matching name/type
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: profile id to start pagination after; default is 0 for first profile"""
        return self.get(**kwargs)

    def retrieve(self, profile_id: str, **kwargs) -> Response:
        """Retrieve one profile.
        :param profile_id: id of the profile"""
        return self.get(profile_id, **kwargs)

    @all_params(_param_kwargs["assign_to_device_group"])
    @param_kwargs(_param_kwargs["assign_to_device_group"])
    @url_suffixes("device_groups", ["device_group_id"])
    def assign_to_device_group(self, profile_id: str, **kwargs) -> Response:
        """Assign a profile to a device group.
        :param profile_id: id of the profile
        :param device_group_id: id of the device group"""
        return self.post(profile_id, **kwargs)

    @all_params(_param_kwargs["assign_to_device_group"])
    @param_kwargs(_param_kwargs["assign_to_device_group"])
    @url_suffixes("device_groups", ["device_group_id"])
    def unassign_from_device_group(self, profile_id: str, **kwargs) -> Response:
        """Unassign a profile from a device group.
        :param profile_id: id of the profile
        :param device_group_id: id of the device group"""
        return self.delete(profile_id, **kwargs)

    @all_params(_param_kwargs["assign_to_device"])
    @param_kwargs(_param_kwargs["assign_to_device"])
    @url_suffixes("devices", ["device_id"])
    def assign_to_device(self, profile_id: str, **kwargs) -> Response:
        """Assign a profile to a device.
        :param profile_id: id of the profile
        :param device_id: id of the device"""
        return self.post(profile_id, **kwargs)

    @all_params(_param_kwargs["assign_to_device"])
    @param_kwargs(_param_kwargs["assign_to_device"])
    @url_suffixes("devices", ["device_id"])
    def unassign_from_device(self, profile_id: str, **kwargs) -> Response:
        """Unassign a profile from a device.
        :param profile_id: id of the profile
        :param device_id: id of the device"""
        return self.delete(profile_id, **kwargs)
