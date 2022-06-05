from .connector import SimpleMDMConnector, APIParamException
from .typers import OptionalDict, UnionIntString
from typing import Any


class CustomConfigProfiles(SimpleMDMConnector):
    """Simple MDM Custom Configuration Profiles.
    https://simplemdm.com/docs/api/#custom-configuration-profiles"""
    def __init__(self, endpoint: str = "custom_configuration_profiles") -> None:
        self.endpoint = endpoint
        super().__init__()

    # To be implemented:

    def assign_to_device_group(self, profile_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Assign a custom configuration profile to a device group.
        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return self.post(url=url, params=params, **kwargs)  # Returns ??

    def unassign_from_device_group(self, profile_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Unassign a custom configuration profile from a device group.
        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return self.delete(url=url, params=params, **kwargs)  # Returns ??

    def assign_to_device(self, profile_id: UnionIntString, grp_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Assign a custom configuration profile to a device group.
        :param profile_id: the id value.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{grp_id}"

        return self.post(url=url, params=params, **kwargs)  # Returns ??

    def unassign_from_device(self, profile_id: UnionIntString, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Unassign a custom configuration profile from a device group.
        :param profile_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{device_id}"

        return self.delete(url=url, params=params, **kwargs)  # Returns ??

    def create(self, params: OptionalDict = dict(), files: OptionalDict = dict(), **kwargs) -> Any:
        """Upload/create a custom configuration profile.
        :param params: specific parameters to provide to the API query.
        :param files: file to upload.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["attribute_support", "mobileconfig", "name", "user_scope"]
        kwargs["required_params"] = ["mobileconfig", "name"]

        if params.get("name") and not params.get("mobileconfig"):
            raise APIParamException("Error: 'name' parameter cannot be used without 'mobileconfig' parameter.")

        return self.post(params=params, files=files, **kwargs)  # Returns ??

    def delete_profile(self, profile_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete a custom configuration profile.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{profile_id}", params=params, **kwargs)  # Returns ??

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all custom configuration profiles.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Returns a list of profile objects

    def retrieve(self, profile_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve one custom configuration profile.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/download"

        return self.get(url=url, params=params, **kwargs)  # Returns ??

    def update(self, profile_id: UnionIntString, params: OptionalDict = dict(), files: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about a custom configuration profile.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param files: file to upload.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["attribute_support", "mobileconfig", "name", "user_scope"]

        return self.patch(url=f"{profile_id}", files=files, params=params, **kwargs)  # Returns ??
