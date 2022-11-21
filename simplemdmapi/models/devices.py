from ..connector import SimpleMDMConnector
from typing import Any, Optional


class ManagedDevices(SimpleMDMConnector):
    """Managed Devices.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#devices
    """
    def __init__(self, endpoint: str = "devices") -> None:
        self.endpoint = endpoint
        super().__init__()

    def create(self, name: str, group_id: str, **kwargs) -> Any:
        """Create a device.

        :param name: the name the device will appear as within SimpleMDM (this is not the host name).
        :param group_id: the group id to assign the device to.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.create, locals, list())
        return self.post(params=params, **kwargs)  # Return new enrollment object with enrollment URL

    def delete(self, device_id: int | str, **kwargs) -> Any:
        """Delete a device.

        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{device_id}", **kwargs)  # Return 204 status

    def list_all(self,
                 search: Optional[str] = None,
                 include_awaiting_enrollment: Optional[bool] = False,
                 include_secret_custom_attributes: Optional[bool] = False,
                 **kwargs) -> Any:
        """List all devices.

        :param search: limit result response to devices that match the optional string value (searches on
                       name, UDID, serial, IMEI, MAC address, or phone number)
        :param include_awaiting_enrolment: include devices that are waiting to be enrolled (default is False)
        :param include_secret_custom_attributes: include ALL custom attributes including those marked
                                                 as secret (default is False)
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.list_all, vals=locals(), ignored_locals=list())
        return self.paginate(params=params, **kwargs)  # Return list of device objects

    def list_profiles(self, device_id: int | str, **kwargs) -> Any:
        """List profiles assigned to the device (per-device profiles excluded).

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/profiles"

        return self.paginate(url=url, **kwargs)  # Return list of profile objects

    def list_installed_apps(self, device_id: int | str, **kwargs) -> Any:
        """List profiles assigned to the device (per-device profiles excluded).

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/installed_apps"

        return self.paginate(url=url, **kwargs)  # Return list of installed app objects

    def list_users(self, device_id: int | str, **kwargs) -> Any:
        """List user accounts on a device (macOS only).

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/users"

        return self.paginate(url=url, **kwargs)  # Return list of user objects

    def delete_user(self,
                    device_id: int | str,
                    user_id: int | str,
                    **kwargs) -> Any:
        """Delete a user from a device (macOS only).

        :param device_id: the id value.
        :param user_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/users/{user_id}"

        # Return 202 status (returns 422 for unsupported devices)
        return self.delete(url=url, **kwargs)

    def retrieve(self, device_id: int | str, include_secret_custom_attributes: Optional[bool] = False, **kwargs) -> Any:
        """Retrieve one application.

        :param device_id: the id value.
        :param include_secret_custom_attributes: return all custom attribute values include those marked
                                                 secret; default is False
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.retrieve, vals=locals(), ignored_locals=list())
        return self.get(url=f"{device_id}", params=params, **kwargs).json()  # Return device object

    def update(self, name: Optional[str] = None, device_name: Optional[str] = None, **kwargs) -> Any:
        """Update a device.

        :param name: the name the device will appear as within SimpleMDM (this is not the host name).
        :param device_name: the host name to use on the device (requires the device to be online).
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.update, vals=locals(), ignored_locals=list())
        return self.patch(params=params, **kwargs)  # Return new enrollment object with enrollment URL

    def get_attributes(self, device_id: int | str,  **kwargs) -> Any:
        """Get custom attributes for a specific device.

        :param device_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/custom_attribute_values"

        return self.get(url=url, **kwargs).json()  # Return custom attribute object

    def set_attribute(self,
                      device_id: int | str,
                      attr_name: str,
                      **kwargs) -> Any:
        """Get custom attributes for a specific device.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/custom_attribute_values/{attr_name}"

        return self.put(url=url, **kwargs).json()  # Return updated custom attribute object

    def push_assigned_apps(self, device_id: int | str, **kwargs) -> Any:
        """Push apps not already installed on da device to that device.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/push_apps"

        return self.post(url=url, **kwargs)  # Return 202 status

    def refresh(self, device_id: int | str, **kwargs) -> Any:
        """Refresh device information and app inventory for a device.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/refresh"

        return self.post(url=url, **kwargs)  # Return 202 status (returns 429 for excessive requests)

    def restart(self, device_id: int | str, **kwargs) -> Any:
        """Send a restart command to a device

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/restart"

        return self.post(url=url, **kwargs)  # Return 202 status

    def shutdown(self, device_id: int | str, **kwargs) -> Any:
        """Send a shutdown command to a device

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/shutdown"

        return self.post(url=url, **kwargs)  # Return 202 status

    def lock(self,
             device_id: int | str,
             message: Optional[str] = None,
             phone_number: Optional[str] = None,
             pin: Optional[str] = None,
             **kwargs) -> Any:
        """Lock a device and optionally display a message and phone number.

        :param device_id: the id value.
        :param message: optional string to display on the lock screen, iOS 7+ and macOS 10.14+ only
        :param phone_number: optional phone number to display on screen
        :param pin: 6 digit number the device will require to be unlocked, required for macOS devices, not
                    supported by iOS
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lock"
        params = self._k2p(self.lock, vals=locals(), ignored_locals=["device_id"])

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def enable_lost_mode(self,
                         device_id: int | str,
                         message: str,
                         phone_number: str,
                         footnote: Optional[str] = None,
                         **kwargs) -> Any:
        """Activate lost mode on a device and optionally display a message and phone number.

        :param device_id: the id value.
        :param message: optional string to display on the lock screen, iOS 7+ and macOS 10.14+ only
        :param phone_number: optional phone number to display on screen
        :param pin: 6 digit number the device will require to be unlocked, required for macOS devices, not
                    supported by iOS
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode"
        params = self._k2p(self.lock, vals=locals(), ignored_locals=["device_id"])

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def disable_lost_mode(self, device_id: int | str, **kwargs) -> Any:
        """Turn lost mode off for a device.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode"

        return self.delete(url=url, **kwargs)  # Return ??

    def play_sound(self, device_id: int | str, **kwargs) -> Any:
        """Play a sound on a device. Only works when the device is in lost mode.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode/play_sound"

        return self.post(url=url, **kwargs)  # Return ??

    def update_location(self, device_id: int | str, **kwargs) -> Any:
        """Request the device provide the current and up-to-date location.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/lost_mode/update_location"

        return self.post(url=url, **kwargs)  # Return ??

    def clear_passcode(self, device_id: int | str, **kwargs) -> Any:
        """Remove the passcode from a device.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/clear_passcode"

        return self.post(url=url, **kwargs)  # Return 202 status

    def clear_firmware_password(self, device_id: int | str, **kwargs) -> Any:
        """Remove a firmware password from a device. Only works if the password was originally set by SimpleMDM.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/clear_firmware_password"

        return self.post(url=url, **kwargs)  # Return 202 status

    def clear_recovery_lock_password(self, device_id: int | str, **kwargs) -> Any:
        """Clear a recovery lock password from a device. Only works if the password was originally set by SimpleMDM.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/clear_recovery_lock_password"

        return self.post(url=url, **kwargs)  # Return 202 status

    def rotate_recovery_lock_password(self, device_id: int | str, **kwargs) -> Any:
        """Rotate a recovery lock password on a device. Only works if the password was originally set by SimpleMDM.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/rotate_recovery_lock_password"

        return self.post(url=url, **kwargs)  # Return 202 status

    def rotate_filevault_key(self, device_id: int | str, **kwargs) -> Any:
        """Rotate the FileVault recovery key of a device. SimpleMDM must be aware of the existing recovery key.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/rotate_filevault_key"

        return self.post(url=url, **kwargs)  # Return 202 status

    def wipe(self, device_id: int | str, pin: int | str, **kwargs) -> Any:
        """Wipe the device (Erase all Contents and Settings). Unenrolls device and returns to factory config.

        The 'pin' parameter must be supplied if the device is a Mac that does not have a T2 chip (presumably
        applies to Apple Silicon?).

        :param device_id: the id value.
        :param pin: the pin to pass to the device to unlock it, required if the Mac does not have a T2 chip,
                    not supported on iOS or Mac if the device has a T2 chip (or Apple Silicon)
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/wipe"
        params = self._k2p(self.wipe, vals=locals(), ignored_locals=["device_id"])

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def update_os(self, device_id: int | str, macos_update_mode: Optional[str] = None, **kwargs) -> Any:
        """Update the device to the latest OS release. Currently only supported by iOS devices.

        :param device_id: the id value.
        :param macos_update_mode: optional for when sending the command to Mac devices, must be one of:
                                   - 'smart_update'
                                   - 'notify_only'
                                   - 'install_asap'
                                   - 'force_update'
                                  this parameter is disregarded if sent to an iOS device
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/update_os"
        params = self._k2p(self.update_os, vals=locals(), ignored_locals=["device_id"])

        return self.post(url=url, params=params, **kwargs)  # Return 202 status

    def enable_remote_desktop(self, device_id: int | str, **kwargs) -> Any:
        """Enable Remote Desktop on the specified device. macOS 10.14.4+ only.

        This call will return a HTTP 400 error if Remote Desktop is already enabled on the target device,
        so the 'ignore_statuses' argument is supplied in the 'post' call to ignore any exception that
        'requests' would raise.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/remote_desktop"

        return self.post(url=url, ignore_statuses=[400], **kwargs)  # Return 202 status

    def disable_remote_desktop(self, device_id: int | str, **kwargs) -> Any:
        """Disable Remote Desktop on the specified device. macOS 10.14.4+ only.

        :param device_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        url = f"{device_id}/remote_desktop"

        return self.delete(url=url, **kwargs)  # Return 202 status
