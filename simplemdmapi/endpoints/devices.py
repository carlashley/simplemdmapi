from requests.models import Response
from typing import Generator, Optional

from ..connector import SimpleMDMConnector
from .._decorators import paginate, url_suffixes
from .._validators import all_digits, params_or_required, pin_length, validate_param_opts


class Devices(SimpleMDMConnector):
    def __init__(self, endpoint: str = "devices") -> None:
        self.endpoint = endpoint
        super().__init__()

    @paginate
    def list_all(
        self,
        search: Optional[str] = None,
        inc_await_enr: Optional[bool] = False,
        inc_secret_attrs: Optional[bool] = True,
        **kwargs,
    ) -> Generator[dict, None, None]:
        """List all devices.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: device id to start pagination after; default is 0 for first device"""
        if search:
            kwargs["params"]["search"] = search

        if inc_await_enr:
            kwargs["params"]["include_awaiting_enrollment"] = inc_await_enr

        if inc_secret_attrs:
            kwargs["params"]["include_secret_custom_attributes"] = inc_secret_attrs

        return self.get(**kwargs)

    def retrieve(self, device_id: str, inc_secret_attrs: bool = True, **kwargs) -> Response:
        """Retrieve one device.
        :param device_id: id of the device
        :param include_secret_custom_attributes: include data for secret custom values; default is True (the
                                                 SimpleMDM default is False)"""
        kwargs["params"] = {"include_secret_custom_attributes": inc_secret_attrs}
        return self.get(device_id, **kwargs)

    def create(self, name: str, group_id: str, **kwargs) -> Response:
        """Create a device.
        :param name: device name that appears within SimpleMDM (this is not the device hostname)
        :param group_id: id of the group to initially assign the device to"""
        kwargs["params"] = {"name": name, "group_id": group_id}
        return self.post(**kwargs)

    @params_or_required(param_keys=["name", "device_name"])
    def update_device(
        self, device_id: str, name: Optional[str] = None, device_name: Optional[str] = None, **kwargs
    ) -> Response:
        """Update name/device name for a device.
        :param device_id: id of the device
        :param include_secret_custom_attributes: include data for secret custom values; default is True (the
                                                 SimpleMDM default is False)"""
        kwargs["params"] = {}

        if name:
            kwargs["params"]["name"] = name

        if device_name:
            kwargs["params"]["device_name"] = device_name

        return self.patch(device_id, **kwargs)

    def remove_device(self, device_id: str) -> Response:
        """Delete a device.
        :param device_id: id of the device"""
        return self.delete(device_id)

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
        return self.get(f"{device_id}/installed_apps", **kwargs)

    @url_suffixes("users")
    @paginate
    def list_users(self, device_id: str, **kwargs) -> Generator[dict, None, None]:
        """List user accounts on a device.
        :param device_id: id of the device"""
        return self.get(f"{device_id}", **kwargs)

    @url_suffixes("users", ["user_id"])
    def delete_user(self, device_id: str, user_id: str, **kwargs) -> Response:
        """Delete a user account from a device.
        :param device_id: id of the device
        :param user_id: id of the user to delete"""
        return self.delete(f"{device_id}", **kwargs)

    @url_suffixes("push_apps")
    def push_apps(self, device_id: str, **kwargs) -> Response:
        """Push assigned apps to a device.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("refresh")
    def refresh(self, device_id: str, **kwargs) -> Response:
        """Refresh device information.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("reboot")
    def restart(
        self,
        device_id: str,
        rebuild_kernel_cache: Optional[bool] = False,
        notify_user: Optional[bool] = False,
        **kwargs,
    ) -> Response:
        """Reboot a device.
        :param device_id: id of the device
        :param rebuild_kernel_cache: optional, rebuild kernal cache on reboot; default is False
        :param notify_user: optional, notify a user if there is one signed in; default is False"""
        kwargs["params"] = {"rebuild_kernel_cache": rebuild_kernel_cache, "notify_user": notify_user}
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("shutdown")
    def shutdown(self, device_id: str, **kwargs) -> Response:
        """Shutdown a device.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @pin_length("pin", 6)
    @all_digits("pin")
    @url_suffixes("lock")
    def lock(
        self,
        device_id: str,
        message: Optional[str] = None,
        phone_num: Optional[str] = None,
        pin: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """Lock a device.
        Note, the 'pin' parameter is required if the target device is a Mac.
        :param device_id: id of the device
        :param message: optional, message string to display on lock screen (iOS 7+, macOS 10.14+)
        :param phone_num: optional, phone number to display on the lock screen
        :param pin: optional (but required for Mac), a 6 digit number the device will require to unlock"""
        kwargs["params"] = {}

        if message:
            kwargs["params"]["message"] = message

        if phone_num:
            kwargs["params"]["phone_number"] = phone_num

        if pin:
            kwargs["params"]["pin"] = pin

        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("clear_passcode")
    def clear_passcode(self, device_id: str, **kwargs) -> Response:
        """Unlock and remove a passcode from a device.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("clear_firmware_password")
    def clear_firmware_password(self, device_id: str, **kwargs) -> Response:
        """Remove firmware password from a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("rotate_firmware_password")
    def rotate_firmware_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the firmware password of a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

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
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("set_admin_password")
    def set_admin_password(self, device_id: str, password: str, **kwargs) -> Response:
        """Set the macOS Auto Admin password for a Mac.
        :param device_id: id of the device
        :param password: password string (cleartext)"""
        kwargs["params"] = {"new_password": password}
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("rotate_admin_password")
    def rotate_admin_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the macOS Auto Admin password for a Mac.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @pin_length("pin", 6)
    @all_digits("pin")
    @url_suffixes("wipe")
    def wipe(self, device_id: str, pin: Optional[str] = None, **kwargs) -> Response:
        """Wipe a device (uses Erase all Content and Settings); device is unenrolled from SimpleMDM and
        restored to a factory default configuration.
        Note: a pin is required for Intel macOS devices that do not have a T2 chip, must be a six digit number
        :param device_id: id of the device
        :param pin: six digit number (for Intel macOS devices that do not have a T2 chip)"""
        return self.post(f"{device_id}", **kwargs)

    @validate_param_opts(
        [
            ("os_update_mode", ["smart_update", "download_only", "notify_only", "install_asap", "force_update"]),
            ("version_type", ["latest_minor_version", "latest_major_version"]),
        ]
    )
    @url_suffixes("update_os")
    def update_os(
        self, device_id: str, os_update_mode: Optional[str] = None, version_type: Optional[str] = None, **kwargs
    ) -> Response:
        """Update the OS on a device.
        Note: the 'os_update_mode' parameter is required for macOS devices, it is ignored by iOS/tvOS/iPadOS devices
        :param device_id: id of the device
        :param os_update_mode: optional string indicating the mode to apply to the update; valid options are:
                               'smart_update', 'download_only', 'notify_only', 'install_asap', 'force_update'
        :param version_type: optional string indicating the update version type to apply; valid options are:
                             'latest_minor_version', 'latest_major_version'; the default is 'latest_major_version'"""
        kwargs["params"] = {}

        if os_update_mode:
            kwargs["params"]["os_update_mode"] = os_update_mode

        if version_type:
            kwargs["params"]["version_type"] = version_type

        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("remote_desktop")
    def enable_remote_desktop(self, device_id: str, **kwargs) -> Response:
        """Enable remote desktop on a device (macOS 10.14.4+ only). This only enables Remote Desktop, it does
        not set any of the ARD permission options.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("remote_desktop")
    def disable_remote_desktop(self, device_id: str, **kwargs) -> Response:
        """Disable remote desktop on a device (macOS 10.14.4+ only). This only disables Remote Desktop, it does
        not unset any of the ARD permission options.
        :param device_id: id of the device"""
        return self.delete(f"{device_id}", **kwargs)

    @url_suffixes("bluetooth")
    def enable_bluetooth(self, device_id: str, **kwargs) -> Response:
        """Enable Bluetooth on a device (iOS 11.3+ and macOS 10.13.4+ only).
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("bluetooth")
    def disable_bluetooth(self, device_id: str, **kwargs) -> Response:
        """Disable Bluetooth on a device (iOS 11.3+ and macOS 10.13.4+ only).
        :param device_id: id of the device"""
        return self.delete(f"{device_id}", **kwargs)

    @url_suffixes("set_time_zone")
    def set_timezone(self, device_id: str, time_zone, **kwargs) -> Response:
        """Set a timezone (using a TZ Identifier value: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
        :param device_id: id of the device
        :param time_zone: string value (TZ Identifier) representing the timezone to set"""
        kwargs["params"] = {"time_zone": time_zone}
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("unenroll")
    def unenroll(self, device_id: str, **kwargs) -> Response:
        """Unenroll a device from SimpleMDM.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("custom_attribute_values")
    def get_device_attributes(self, device_id: str, **kwargs) -> Response:
        """Get custom attributes for a device.
        :param device_id: id of the device"""
        return self.get(f"{device_id}", **kwargs)

    @url_suffixes("custom_attribute_values", ["attr_name"])
    def set_device_attribute(self, device_id: str, attr_name: str, attr_value: str, **kwargs) -> Response:
        """Set custom attribute value for a device.
        :param device_id: id of the device
        :param attr_name: the custom attribute name
        :param attr_value: the value to apply to the custom attribute for the device"""
        kwargs["params"] = {"value": attr_value}
        return self.get(f"{device_id}", **kwargs)

    @url_suffixes("lost_mode")
    def enable_lost_mode(self, device_id: str, **kwargs) -> Response:
        """Enable lost mode on a device.
        :param device_id: id of the device"""
        return self.post(f"{device_id}", **kwargs)

    @url_suffixes("lost_mode")
    def disable_lost_mode(self, device_id: str, **kwargs) -> Response:
        """Disable lost mode on a device.
        :param device_id: id of the device"""
        return self.delete(f"{device_id}", **kwargs)

    @url_suffixes("lost_mode/play_sound")
    def play_sound(self, device_id: str, **kwargs) -> Response:
        """Play sound on a device to assit with locating it.
        :param device_id: id of the device"""
        return self.delete(f"{device_id}", **kwargs)

    @url_suffixes("lost_mode/update_location")
    def update_location(self, device_id: str, **kwargs) -> Response:
        """Play sound on a device to assit with locating it.
        :param device_id: id of the device"""
        return self.delete(f"{device_id}", **kwargs)
