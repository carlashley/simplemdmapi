from .connector import SimpleMDMConnector, APIParamException
from .typers import (OptionalDict,
                     UnionIntString)
from typing import Any


class CustomConfigProfiles(SimpleMDMConnector):
    """Simple MDM Custom Configuration Profiles"""
    def __init__(self, endpoint: str = "custom_configuration_profiles") -> None:
        self.endpoint = endpoint
        super().__init__()

    # To be implemented:
        # Assign to device group
        # Unassign from device group
        # Assign to device
        # Unassign from device

    def assign_to_device_group(self, profile_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Assign a custom configuration profile to a device group.
        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()

    def unassign_from_device_group(self, profile_id: UnionIntString, device_grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Unassign a custom configuration profile from a device group.
        :param profile_id: the id value.
        :param device_grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/device_groups/{device_grp_id}"

        return SimpleMDMConnector.delete(url=url)(lambda _: (params, kwargs))(self).json()

    def assign_to_device(self, profile_id: UnionIntString, grp_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Assign a custom configuration profile to a device group.
        :param profile_id: the id value.
        :param grp_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{grp_id}"

        return SimpleMDMConnector.post(url=url)(lambda _: (params, kwargs))(self).json()

    def unassign_from_device(self, profile_id: UnionIntString, device_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Unassign a custom configuration profile from a device group.
        :param profile_id: the id value.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/devices/{device_id}"

        return SimpleMDMConnector.delete(url=url)(lambda _: (params, kwargs))(self).json()

    @SimpleMDMConnector.post(filename_key="mobileconfig")
    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Upload/create a custom configuration profile.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["attribute_support", "mobileconfig", "name", "user_scope"]
        reqrd_params = ["mobileconfig", "name"]
        name = params.get("name")
        binary = params.get("mobileconfig")
        self.validate_params(params, valid_params)
        self.required_params(params, reqrd_params)

        if name and not binary:
            raise APIParamException("Error: 'name' parameter cannot be used without 'mobileconfig' parameter.")

        self.validate_file_extensions(binary, [".mobileconfig", ".txt", ".plist"])
        kwargs["files"] = {"mobileconfig": binary}
        del params["mobileconfig"]

        return params, kwargs

    def delete_profile(self, profile_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete a custom configuration profile.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return SimpleMDMConnector.delete(url=profile_id)(lambda _: (params, kwargs))(self)

    @SimpleMDMConnector.paginate()
    def list_all(self, params: OptionalDict, **kwargs) -> Any:
        """List all custom configuration profiles.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return params, kwargs

    def list_installs(self, profile_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """List all custom configuration profiles.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/installs"

        return SimpleMDMConnector.paginate(url=url)(lambda _: (params, kwargs))(self)

    def retrieve(self, profile_id: UnionIntString, params: OptionalDict, **kwargs) -> Any:
        """Retrieve one custom configuration profile.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{profile_id}/download"

        return SimpleMDMConnector.get(url=url)(lambda _: (params, kwargs))(self).json()

    def update(self, profile_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update details about a custom configuration profile.
        :param profile_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        valid_params = ["attribute_support", "mobileconfig", "name", "user_scope"]
        binary = params.get("mobileconfig")
        self.validate_params(params, valid_params)

        if binary:
            self.validate_file_extensions(binary, [".mobileconfig", ".txt", ".plist"])
            kwargs["files"] = {"mobileconfig": binary}
            del params["mobileconfig"]

        return SimpleMDMConnector.patch(url=profile_id, filename_key="mobileconfig")(lambda _: (params, kwargs))(self).json()
