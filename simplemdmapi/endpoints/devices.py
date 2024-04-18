from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate, url_suffixes
from ..validators import validate_pin


class Devices(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#devices"""

    def __init__(self, endpoint: str = "devices", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": [
                    "search",
                    "include_awaiting_enrollment",
                    "include_secret_custom_attributes",
                    "limit",
                    "starting_after",
                ],
            },
            "retrieve": {
                "all_params": ["include_secret_custom_attributes"],
            },
            "create": {
                "all_params": ["name", "group_id"],
                "req_params": ["name"],
            },
            "update": {
                "all_params": ["device_name", "name"],
                "any_params": ["device_name", "name"],
            },
            "delete_user": {
                "all_params": ["user_id"],
                "req_params": ["user_id"],
            },
            "reboot": {
                "all_params": ["notify_user", "rebuild_kernel_cache"],
                "validate": {
                    "rebuild_kernel_cache": [True, False],
                    "notify_user": [True, False],
                },
            },
            "lock": {
                "all_params": ["message", "phone_number", "pin"],
            },
            "set_admin_password": {
                "all_params": ["new_password"],
                "req_params": ["new_password"],
            },
            "wipe": {
                "all_params": ["pin"],
            },
            "update_os": {
                "all_params": ["os_update_mode", "version_type"],
                "validate": {
                    "os_update_mode": ["download_only", "force_update", "install_asap", "smart_update", "notify_only"],
                    "version_type": ["latest_major_version", "latest_minor_version"],
                },
            },
            "set_timezone": {
                "all_params": ["time_zone"],
                "req_params": ["time_zone"],
            },
            "set_device_attributes": {
                "all_params": ["attr_name", "value"],
                "req_params": ["attr_name", "value"],
            },
            "set_multiple_device_attributes": {
                "all_params": ["json"],
                "req_params": ["json"],
            },
            "enable_lost_mode": {
                "all_params": ["message", "phone_number", "footnote"],
                "any_params": ["message", "phone_number", "footnote"],
            },
        }

    @method_params
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all devices.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: device id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    @method_params
    def retrieve(self, device_id: str, **kwargs) -> Response:
        """Retrieve one device.
        :param device_id: id of the device
        :param include_secret_custom_attributes: include data for secret custom values; default is True (the
                                                 SimpleMDM default is False)"""
        return self.get(device_id, **kwargs)

    @method_params
    def create(self, **kwargs) -> Response:
        """Create a device.
        :param name: device name that appears within SimpleMDM (this is not the device hostname)
        :param group_id: id of the group to initially assign the device to"""
        return self.post(**kwargs)

    @method_params
    def update(self, device_id: str, **kwargs) -> Response:
        """Update name/device name for a device.
        :param device_id: id of the device
        :param name: device name that appears within SimpleMDM (this is not the device hostname)
        :param device_name: the device hostname"""
        return self.patch(device_id, **kwargs)

    def remove(self, device_id: str, **kwargs) -> Response:
        """Delete a device.
        :param device_id: id of the device"""
        return self.delete(device_id, **kwargs)

    @url_suffixes("profiles")
    @paginate
    def list_profiles(self, device_id: str, **kwargs) -> Generator[dict, None, None]:
        """List profiles assigned to a device.
        :param device_id: id of the device"""
        return self.get(f"{device_id}/profiles", **kwargs)

    @url_suffixes("installed_apps")
    @paginate
    def list_applications(self, device_id: str, **kwargs) -> Generator[dict, None, None]:
        """List applications installed on a device
        :param device_id: id of the device"""
        return self.get(device_id, **kwargs)

    @url_suffixes("users")
    @paginate
    def list_users(self, device_id: str, **kwargs) -> Generator[dict, None, None]:
        """List user accounts on a device.
        :param device_id: id of the device"""
        return self.get(device_id, **kwargs)

    @method_params
    @url_suffixes("users", ["user_id"])
    def delete_user(self, device_id: str, **kwargs) -> Response:
        """Delete a user account from a device.
        :param device_id: id of the device
        :param user_id: id of the user to delete"""
        return self.delete(device_id, **kwargs)

    @url_suffixes("push_apps")
    def push_apps(self, device_id: str, **kwargs) -> Response:
        """Push assigned apps to a device.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("refresh")
    def refresh(self, device_id: str, **kwargs) -> Response:
        """Refresh device information.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @method_params
    @url_suffixes("reboot")
    def restart(self, device_id: str, **kwargs) -> Response:
        """Reboot a device.
        :param device_id: id of the device
        :param rebuild_kernel_cache: optional, rebuild kernal cache on reboot; default is False
        :param notify_user: optional, notify a user if there is one signed in; default is False"""
        return self.post(device_id, **kwargs)

    @url_suffixes("shutdown")
    def shutdown(self, device_id: str, **kwargs) -> Response:
        """Shutdown a device.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @method_params
    @validate_pin("pin", 6)
    @url_suffixes("lock")
    def lock(self, device_id: str, **kwargs) -> Response:
        """Lock a device.
        Note, the 'pin' parameter is required if the target device is a Mac.
        :param device_id: id of the device
        :param message: optional, message string to display on lock screen (iOS 7+, macOS 10.14+)
        :param phone_number: optional, phone number to display on the lock screen
        :param pin: optional (but required for Mac), a 6 digit number the device will require to unlock"""
        return self.post(device_id, **kwargs)

    @url_suffixes("clear_passcode")
    def clear_passcode(self, device_id: str, **kwargs) -> Response:
        """Unlock and remove a passcode from a device.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("clear_firmware_password")
    def clear_firmware_password(self, device_id: str, **kwargs) -> Response:
        """Remove firmware password from a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("rotate_firmware_password")
    def rotate_firmware_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the firmware password of a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("clear_recovery_lock_password")
    def clear_recovery_lock_password(self, device_id: str, **kwargs) -> Response:
        """Remove recovery lock password from a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device"""
        return self.post(f"{device_id}/clear_recovery_lock_password", **kwargs)

    @url_suffixes("rotate_recovery_lock_password")
    def rotate_recovery_lock_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the recovery lock password of a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device"""
        return self.post(f"{device_id}/rotate_recovery_lock_password", **kwargs)

    @url_suffixes("rotate_filevault_key")
    def rotate_fielvault_recovery_key(self, device_id: str, **kwargs) -> Response:
        """Rotate the FileVault recovery key of a device (SimpleMDM must be aware of the current recovery key)
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @method_params
    @url_suffixes("set_admin_password")
    def set_admin_password(self, device_id: str, **kwargs) -> Response:
        """Set the macOS Auto Admin password for a Mac.
        :param device_id: id of the device
        :param new_password: password string (cleartext)"""
        return self.post(device_id, **kwargs)

    @url_suffixes("rotate_admin_password")
    def rotate_admin_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the macOS Auto Admin password for a Mac.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @method_params
    @validate_pin("pin", 6)
    @url_suffixes("wipe")
    def wipe(self, device_id: str, **kwargs) -> Response:
        """Wipe a device (uses Erase all Content and Settings); device is unenrolled from SimpleMDM and
        restored to a factory default configuration.
        Note: a pin is required for Intel macOS devices that do not have a T2 chip, must be a six digit number
        :param device_id: id of the device
        :param pin: optional six digit number (for Intel macOS devices that do not have a T2 chip)"""
        return self.post(device_id, **kwargs)

    @method_params
    @url_suffixes("update_os")
    def update_os(self, device_id: str, **kwargs) -> Response:
        """Update the OS on a device.
        Note: the 'os_update_mode' parameter is required for macOS devices, it is ignored by iOS/tvOS/iPadOS devices
        :param device_id: id of the device
        :param os_update_mode: optional string indicating the mode to apply to the update; valid options are:
                               'smart_update', 'download_only', 'notify_only', 'install_asap', 'force_update'
        :param version_type: optional string indicating the update version type to apply; valid options are:
                             'latest_minor_version', 'latest_major_version'; the default is 'latest_major_version'"""
        return self.post(device_id, **kwargs)

    @url_suffixes("remote_desktop")
    def enable_remote_desktop(self, device_id: str, **kwargs) -> Response:
        """Enable remote desktop on a device (macOS 10.14.4+ only). This only enables Remote Desktop, it does
        not set any of the ARD permission options.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("remote_desktop")
    def disable_remote_desktop(self, device_id: str, **kwargs) -> Response:
        """Disable remote desktop on a device (macOS 10.14.4+ only). This only disables Remote Desktop, it does
        not unset any of the ARD permission options.
        :param device_id: id of the device"""
        return self.delete(device_id, **kwargs)

    @url_suffixes("bluetooth")
    def enable_bluetooth(self, device_id: str, **kwargs) -> Response:
        """Enable Bluetooth on a device (iOS 11.3+ and macOS 10.13.4+ only).
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("bluetooth")
    def disable_bluetooth(self, device_id: str, **kwargs) -> Response:
        """Disable Bluetooth on a device (iOS 11.3+ and macOS 10.13.4+ only).
        :param device_id: id of the device"""
        return self.delete(device_id, **kwargs)

    @method_params
    @url_suffixes("set_time_zone")
    def set_timezone(self, device_id: str, **kwargs) -> Response:
        """Set a timezone (using a TZ Identifier value: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
        :param device_id: id of the device
        :param time_zone: string value (TZ Identifier) representing the timezone to set"""
        return self.post(device_id, **kwargs)

    @url_suffixes("unenroll")
    def unenroll(self, device_id: str, **kwargs) -> Response:
        """Unenroll a device from SimpleMDM.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("custom_attribute_values")
    def get_device_attributes(self, device_id: str, **kwargs) -> Response:
        """Get custom attributes for a device.
        :param device_id: id of the device"""
        return self.get(device_id, **kwargs)

    @method_params
    @url_suffixes("custom_attribute_values", ["attr_name"])
    def set_device_attribute(self, device_id: str, **kwargs) -> Response:
        """Set custom attribute value for a device.
        :param device_id: id of the device
        :param attr_name: the custom attribute name
        :param value: the value to apply to the custom attribute for the device"""
        return self.get(device_id, **kwargs)

    @method_params
    @url_suffixes("custom_attribute_values")
    def set_multiple_device_attributes(self, device_id: str, **kwargs) -> Response:
        """Set multiple custom attribute values for a device.
        :param device_id: id of the device
        :param json: dictionary object that is passed to requests to convert to JSON"""
        return self.put(device_id)

    @method_params
    @url_suffixes("lost_mode")
    def enable_lost_mode(self, device_id: str, **kwargs) -> Response:
        """Enable lost mode on a device.
        :param device_id: id of the device"""
        return self.post(device_id, **kwargs)

    @url_suffixes("lost_mode")
    def disable_lost_mode(self, device_id: str, **kwargs) -> Response:
        """Disable lost mode on a device.
        :param device_id: id of the device"""
        return self.delete(device_id, **kwargs)

    @url_suffixes("lost_mode/play_sound")
    def play_sound(self, device_id: str, **kwargs) -> Response:
        """Play sound on a device to assit with locating it.
        :param device_id: id of the device"""
        return self.delete(device_id, **kwargs)

    @url_suffixes("lost_mode/update_location")
    def update_location(self, device_id: str, **kwargs) -> Response:
        """Play sound on a device to assit with locating it.
        :param device_id: id of the device"""
        return self.delete(device_id, **kwargs)
