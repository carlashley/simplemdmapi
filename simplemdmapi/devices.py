from .connector import SimpleMDMConnector
from .typehints import OptionalDict, UnionIntString
from typing import Any


class ManagedDevices(SimpleMDMConnector):
    """Simple MDM Managed Devices.
    https://simplemdm.com/docs/api/#devices"""
    def __init__(self, endpoint: str = "devices") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Create a device.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["group_id", "name"]

        return self.post(params=params, **kwargs)  # Return new enrollment object with enrollment URL

    def delete(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete a device.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{device_id}", params=params, **kwargs)  # Return 204 status

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all devices.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["include_awaiting_enrollment", "search"]

        return self.paginate(params=params, **kwargs)  # Return list of device objects

    def list_profiles(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """List profiles assigned to the device (per-device profiles excluded).
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/profiles"

        return self.paginate(url=url, params=params, **kwargs)  # Return list of profile objects

    def list_installed_apps(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """List profiles assigned to the device (per-device profiles excluded).
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/installed_apps"

        return self.paginate(url=url, params=params, **kwargs)  # Return list of installed app objects

    def list_users(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """List user accounts on a device (macOS only).
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/users"

        return self.paginate(url=url, params=params, **kwargs)  # Return list of user objects

    def delete_user(self, device_id: UnionIntString, user_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete a user from a device (macOS only).
        :param device_id: the id value.
        :param user_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/users/{user_id}"

        return self.paginate(url=url, params=params, **kwargs)  # Return 202 status (returns 422 for unsupported devices)

    def retrieve(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Retrieve one application.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{device_id}", params=params, **kwargs).json()  # Return device object

    def update(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update a device.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["device_name", "name"]

        return self.patch(params=params, **kwargs)  # Return device object

    def get_attribute(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Get custom attributes for a specific device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/custom_attribute_values"

        return self.get(url=url, params=params, **kwargs).json()  # Return custom attribute object

    def set_attribute(self, device_id: UnionIntString, attr_name: str, params: OptionalDict = dict(), **kwargs) -> Any:
        """Get custom attributes for a specific device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        reqrd_params = ["value"]
        self.validate_params(params, reqrd_params)
        self.required_params(params, reqrd_params)

        url = f"{device_id}/custom_attribute_values/{attr_name}"
        return self.put(url=url, params=params, **kwargs).json()  # Return updated custom attribute object

    def push_assigned_apps(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Push apps not already installed on da device to that device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/push_apps"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def refresh(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Refresh device information and app inventory for a device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/refresh"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status (returns 429 for excessive requests)

    def restart(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Send a restart command to a device
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["notify_user", "rebuild_kernel_cache"]
        url = f"{device_id}/restart"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def shutdown(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Send a shutdown command to a device
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/shutdown"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def lock(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Lock a device and optionally display a message and phone number.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["message", "phone_number", "pin"]
        url = f"{device_id}/lock"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def enable_lost_mode(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Turn lost mode on for a device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["required_params"] = ["message"]  # Technically message OR phone number
        kwargs["validate_params"] = ["footnote", "message", "phone_number"]
        url = f"{device_id}/lost_mode"

        return self.post(url=url, params=params, **kwargs)  # Return ??

    def disable_lost_mode(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Turn lost mode off for a device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode"

        return self.delete(url=url, params=params, **kwargs)  # Return ??

    def play_sound(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Play a sound on a device. Only works when the device is in lost mode.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode/play_sound"

        return self.post(url=url, params=params, **kwargs)  # Return ??

    def update_location(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Request the device provide the current and up-to-date location.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode/update_location"

        return self.post(url=url, params=params, **kwargs)  # Return ??

    def clear_passcode(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Remove the passcode from a device.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/clear_passcode"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def clear_firmware_password(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Remove a firmware password from a device. Only works if the password was originally set by SimpleMDM.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/clear_firmware_password"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def rotate_filevault_key(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Rotate the FileVault recovery key of a device. SimpleMDM must be aware of the existing recovery key.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/rotate_filevault_key"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def wipe(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Wipe the device (Erase all Contents and Settings). Unenrolls device and returns to factory config.
        The 'pin' parameter must be supplied if the device is a Mac that does not have a T2 chip (presumably
        applies to Apple Silicon?).
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["validate_params"] = ["pin"]
        url = f"{device_id}/wipe"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def update_os(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Update the device to the latest OS release. Currently only supported by iOS devices.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/update_os"

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def enable_remote_desktop(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Enable Remote Desktop on the specified device. macOS 10.14.4+ only.
        This call will return a HTTP 400 error if Remote Desktop is already enabled on the target device,
        so the 'ignore_statuses' argument is supplied in the 'post' call to ignore any exception that
        'requests' would raise.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/remote_desktop"

        return self.post(url=url, params=params, ignore_statuses=[400], **kwargs)  # Return 202 status

    def disable_remote_desktop(self, device_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Disable Remote Desktop on the specified device. macOS 10.14.4+ only.
        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/remote_desktop"

        return self.delete(url=url, params=params, **kwargs)  # Return 202 status
