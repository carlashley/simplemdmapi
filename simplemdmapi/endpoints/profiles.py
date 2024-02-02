from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate, url_suffixes


class Profiles(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#profiles"""

    def __init__(self, endpoint: str = "profiles", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
            "assign_to_device_group": {
                "all_params": ["device_group_id"],
                "req_params": ["device_group_id"],
            },
            "unassign_from_device_group": {
                "all_params": ["device_group_id"],
                "req_params": ["device_group_id"],
            },
            "assign_to_device": {
                "all_params": ["device_id"],
                "req_params": ["device_id"],
            },
            "unassign_from_device": {
                "all_params": ["device_id"],
                "req_params": ["device_id"],
            },
        }

    @method_params
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

    @method_params
    @url_suffixes("device_groups", ["device_group_id"])
    def assign_to_device_group(self, profile_id: str, **kwargs) -> Response:
        """Assign a profile to a device group.
        :param profile_id: id of the profile
        :param device_group_id: id of the device group"""
        return self.post(profile_id, **kwargs)

    @method_params
    @url_suffixes("device_groups", ["device_group_id"])
    def unassign_from_device_group(self, profile_id: str, **kwargs) -> Response:
        """Unassign a profile from a device group.
        :param profile_id: id of the profile
        :param device_group_id: id of the device group"""
        return self.delete(profile_id, **kwargs)

    @method_params
    @url_suffixes("devices", ["device_id"])
    def assign_to_device(self, profile_id: str, **kwargs) -> Response:
        """Assign a profile to a device.
        :param profile_id: id of the profile
        :param device_id: id of the device"""
        return self.post(profile_id, **kwargs)

    @method_params
    @url_suffixes("devices", ["device_id"])
    def unassign_from_device(self, profile_id: str, **kwargs) -> Response:
        """Unassign a profile from a device.
        :param profile_id: id of the profile
        :param device_id: id of the device"""
        return self.delete(profile_id, **kwargs)
