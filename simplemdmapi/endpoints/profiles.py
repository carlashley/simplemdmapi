from typing import Optional
from requests.models import Response
from ..connector import SimpleMDMConnector


class CustomConfigProfiles(SimpleMDMConnector):
    """Custom Configuration Profiles.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#custom-configuration-profiles
    """
    def __init__(self, endpoint: str = "custom_configuration_profiles") -> None:
        self.endpoint = endpoint
        super().__init__()

    # To be implemented:

    def assign_to_device_group(self,
                               profile_id: int | str,
                               device_grp_id: int | str,
                               **kwargs) -> Response:
        """Assign a custom configuration profile to a device group.

        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return self.post(url=url, **kwargs)  # Returns ??

    def unassign_from_device_group(self,
                                   profile_id: int | str,
                                   device_grp_id: int | str,
                                   **kwargs) -> Response:
        """Unassign a custom configuration profile from a device group.

        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return self.delete(url=url, **kwargs)  # Returns ??

    def assign_to_device(self,
                         profile_id: int | str,
                         grp_id: int | str,
                         **kwargs) -> Response:
        """Assign a custom configuration profile to a device group.

        :param profile_id: the id value.
        :param grp_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{grp_id}"

        return self.post(url=url, **kwargs)  # Returns ??

    def unassign_from_device(self,
                             profile_id: int | str,
                             device_id: int | str,
                             **kwargs) -> Response:
        """Unassign a custom configuration profile from a device group.

        :param profile_id: the id value.
        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{device_id}"

        return self.delete(url=url, **kwargs)  # Returns ??

    def create(self,
               name: str = None,
               mobileconfig: str = None,
               user_scope: Optional[bool] = False,
               attribute_support: Optional[bool] = False,
               **kwargs) -> Response:
        """Create a custom configuration profile.

        :param name: the name of the profile
        :param mobileconfig: the mobile config itself
        :param user_scope: if False, deploy as a device profile instead of a user profile (True); default is False
        :param attribute_support: enable attribute support in the uploaded profile (True); default is False
        :param kwargs: specific parameters to provide to the underlying requests function."""
        files = {"mobileconfig": mobileconfig}
        params = self._k2p(self.update, vals=locals(), ignored_locals=["profile_id"])
        return self.patch(files=files, params=params, **kwargs)  # Returns ??

    def delete_profile(self, profile_id: int | str, **kwargs) -> Response:
        """Delete a custom configuration profile.

        :param profile_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{profile_id}", **kwargs)  # Returns ??

    def list_all(self, **kwargs) -> Response:
        """List all custom configuration profiles.

        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(**kwargs)  # Returns a list of profile objects

    def retrieve(self, profile_id: int | str, **kwargs) -> Response:
        """Retrieve one custom configuration profile.

        :param profile_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/download"

        return self.get(url=url, **kwargs)  # Returns ??

    def update(self,
               profile_id: int | str,
               name: Optional[str] = None,
               mobileconfig: Optional[str] = None,
               user_scope: Optional[bool] = False,
               attribute_support: Optional[bool] = False,
               **kwargs) -> Response:
        """Update details about a custom configuration profile.

        :param profile_id: the id value.
        :param name: update the name of the profile
        :param mobileconfig: update the mobile config itself
        :param user_scope: if False, deploy as a device profile instead of a user profile (True); default is False
        :param attribute_support: enable attribute support in the uploaded profile (True); default is False
        :param kwargs: specific parameters to provide to the underlying requests function."""
        files = {"mobileconfig": mobileconfig}
        params = self._k2p(self.update, vals=locals(), ignored_locals=["profile_id"])
        return self.patch(url=f"{profile_id}", files=files, params=params, **kwargs)  # Returns ??


class Profiles(SimpleMDMConnector):
    """Profiles.
    Note: These are the 'native' profiles created in the SimpleMDM management dashboard.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/profiles
    """
    def __init__(self, endpoint: str = "profiles") -> None:
        self.endpoint = endpoint
        super().__init__()

    # To be implemented:

    def assign_to_device_group(self,
                               profile_id: int | str,
                               device_grp_id: int | str,
                               **kwargs) -> Response:
        """Assign a profile to a device group.

        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return self.post(url=url, **kwargs)  # Returns ??

    def unassign_from_device_group(self,
                                   profile_id: int | str,
                                   device_grp_id: int | str,
                                   **kwargs) -> Response:
        """Unassign a profile from a device group.

        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return self.delete(url=url, **kwargs)  # Returns ??

    def assign_to_device(self,
                         profile_id: int | str,
                         grp_id: int | str,
                         **kwargs) -> Response:
        """Assign a profile to a device group.

        :param profile_id: the id value.
        :param grp_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{grp_id}"

        return self.post(url=url, **kwargs)  # Returns ??

    def unassign_from_device(self,
                             profile_id: int | str,
                             device_id: int | str,
                             **kwargs) -> Response:
        """Unassign a profile from a device group.

        :param profile_id: the id value.
        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{device_id}"

        return self.delete(url=url, **kwargs)  # Returns ??

    def list_all(self, search: Optional[str] = None, **kwargs) -> Response:
        """List all profiles.

        :param search: optional string to search profiles by name/type
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.list_all, vals=locals(), ignored_locals=list())
        return self.paginate(**kwargs)  # Returns a list of profile objects
