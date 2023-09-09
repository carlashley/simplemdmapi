from requests.models import Response
from typing import Generator, Optional

from ..connector import SimpleMDMConnector
from .._decorators import paginate, api_path_suffix
from .._validators import all_digits, params_or_required, pin_length, validate_param_opts


class Devices(SimpleMDMConnector):
    def __init__(self, endpoint: str = "devices") -> None:
        self.endpoint = endpoint
        super().__init__()

    @paginate
    def list_all(
        self,
        limit: int = 100,
        starting_after: int = 0,
        search: Optional[str] = None,
        inc_await_enr: Optional[bool] = False,
        inc_secret_attrs: Optional[bool] = True,
        **kwargs,
    ) -> Generator[dict, None, None]:
        """List all devices.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: device id to start pagination after; default is 0 for first device"""
        params = {"limit": limit, "starting_after": starting_after}

        if search:
            params["search"] = search

        if inc_await_enr:
            params["include_awaiting_enrollment"] = inc_await_enr

        if inc_secret_attrs:
            params["include_secret_custom_attributes"] = inc_secret_attrs

        return self.get(params=params, **kwargs)

    def retrieve(self, device_id: str, inc_secret_attrs: bool = True, **kwargs) -> Response:
        """Retrieve one device.
        :param device_id: id of the device to retrieve
        :param include_secret_custom_attributes: include data for secret custom values; default is True (the
                                                 SimpleMDM default is False)"""
        params = {"include_secret_custom_attributes": inc_secret_attrs}
        return self.get(device_id, params=params, **kwargs)

    def create(self, name: str, group_id: str, **kwargs) -> Response:
        """Create a device.
        :param name: device name that appears within SimpleMDM (this is not the device hostname)
        :param group_id: id of the group to initially assign the device to"""
        params = {"name": name, "group_id": group_id}
        return self.post(params=params, **kwargs)

    @params_or_required(param_keys=["name", "device_name"])
    def update(
        self, device_id: str, name: Optional[str] = None, device_name: Optional[str] = None, **kwargs
    ) -> Response:
        """Retrieve one device.
        :param device_id: id of the device to retrieve
        :param include_secret_custom_attributes: include data for secret custom values; default is True (the
                                                 SimpleMDM default is False)"""
        params = {}

        if name:
            params["name"] = name

        if device_name:
            params["device_name"] = device_name

        return self.patch(device_id, params=params, **kwargs)

    def remove(self, device_id: str) -> Response:
        """Delete a device.
        :param device_id: id of the device to delete"""
        return self.delete(device_id)

    @paginate
    def list_profiles(
        self, device_id: str, limit: int = 100, starting_after: int = 0, **kwargs
    ) -> Generator[dict, None, None]:
        """List profiles assigned to a device.
        :param device_id: id of the device to list profiles"""
        params = {"limit": limit, "starting_after": starting_after}
        return self.get(f"{device_id}/profiles", params=params, **kwargs)

    @api_path_suffix("installed_apps")
    @paginate
    def list_applications(
        self, device_id: str, limit: int = 100, starting_after: int = 0, **kwargs
    ) -> Generator[dict, None, None]:
        """List applications installed on a device
        :param device_id: id of the device to list applications"""
        params = {"limit": limit, "starting_after": starting_after}
        return self.get(f"{device_id}/installed_apps", params=params, **kwargs)

    @api_path_suffix("users")
    @paginate
    def list_users(
        self, device_id: str, limit: int = 100, starting_after: int = 0, **kwargs
    ) -> Generator[dict, None, None]:
        """List user accounts on a device.
        :param device_id: id of the device to list user accounts"""
        params = {"limit": limit, "starting_after": starting_after}
        return self.get(f"{device_id}", params=params, **kwargs)

    @api_path_suffix("users", ["user_id"])
    def delete_user(self, device_id: str, user_id: str, **kwargs) -> Response:
        """Delete a user account from a device.
        :param device_id: id of the device to delete user account from
        :param user_id: id of the user to delete"""
        return self.delete(f"{device_id}", **kwargs)

    @api_path_suffix("push_apps")
    def push_apps(self, device_id: str, **kwargs) -> Response:
        """Push assigned apps to a device.
        :param device_id: id of the device to push assigned apps to"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("refresh")
    def refresh(self, device_id: str, **kwargs) -> Response:
        """Refresh device information.
        :param device_id: id of the device to refresh"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("reboot")
    def restart(
        self,
        device_id: str,
        rebuild_kernel_cache: Optional[bool] = False,
        notify_user: Optional[bool] = False,
        **kwargs,
    ) -> Response:
        """Reboot a device.
        :param device_id: id of the device to reboot
        :param rebuild_kernel_cache: optional, rebuild kernal cache on reboot; default is False
        :param notify_user: optional, notify a user if there is one signed in; default is False"""
        params = {"rebuild_kernel_cache": rebuild_kernel_cache, "notify_user": notify_user}
        return self.post(f"{device_id}", params=params, **kwargs)

    @api_path_suffix("shutdown")
    def shutdown(self, device_id: str, **kwargs) -> Response:
        """Shutdown a device.
        :param device_id: id of the device to shutdown"""
        return self.post(f"{device_id}", **kwargs)

    @pin_length("pin", 6)
    @all_digits("pin")
    @api_path_suffix("lock")
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
        :param device_id: id of the device to lock
        :param message: optional, message string to display on lock screen (iOS 7+, macOS 10.14+)
        :param phone_num: optional, phone number to display on the lock screen
        :param pin: optional (but required for Mac), a 6 digit number the device will require to unlock"""
        params = {}

        if message:
            params["message"] = message

        if phone_num:
            params["phone_number"] = phone_num

        if pin:
            params["pin"] = pin

        return self.post(f"{device_id}", params=params, **kwargs)

    @api_path_suffix("clear_passcode")
    def clear_passcode(self, device_id: str, **kwargs) -> Response:
        """Unlock and remove a passcode from a device.
        :param device_id: id of the device to unlock/clear passcode"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("clear_firmware_password")
    def clear_firmware_password(self, device_id: str, **kwargs) -> Response:
        """Remove firmware password from a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device to remove firmware password from"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("rotate_firmware_password")
    def rotate_firmware_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the firmware password of a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device to rotate the firmware password for"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("clear_recovery_lock_password")
    def clear_recovery_lock_password(self, device_id: str, **kwargs) -> Response:
        """Remove recovery lock password from a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device to remove firmware password from"""
        return self.post(f"{device_id}/clear_recovery_lock_password", **kwargs)

    @api_path_suffix("rotate_recovery_lock_password")
    def rotate_recovery_lock_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the recovery lock password of a device (password must have been originally set by SimpleMDM)
        :param device_id: id of the device to rotate the firmware password for"""
        return self.post(f"{device_id}/rotate_recovery_lock_password", **kwargs)

    @api_path_suffix("rotate_filevault_key")
    def rotate_fielvault_recovery_key(self, device_id: str, **kwargs) -> Response:
        """Rotate the FileVault recovery key of a device (SimpleMDM must be aware of the current recovery key)
        :param device_id: id of the device to rotate the firmware password for"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("set_admin_password")
    def set_admin_password(self, device_id: str, password: str, **kwargs) -> Response:
        """Set the macOS Auto Admin password for a Mac.
        :param device_id: id of the device to set the admin password
        :param password: password string (cleartext)"""
        params = {"new_password": password}
        return self.post(f"{device_id}", params=params, **kwargs)

    @api_path_suffix("rotate_admin_password")
    def rotate_admin_password(self, device_id: str, **kwargs) -> Response:
        """Rotate the macOS Auto Admin password for a Mac.
        :param device_id: id of the device to rotate the admin password"""
        return self.post(f"{device_id}", **kwargs)

    @pin_length("pin", 6)
    @all_digits("pin")
    @api_path_suffix("wipe")
    def wipe(self, device_id: str, pin: Optional[str] = None, **kwargs) -> Response:
        """Wipe a device (uses Erase all Content and Settings); device is unenrolled from SimpleMDM and
        restored to a factory default configuration.
        Note: a pin is required for Intel macOS devices that do not have a T2 chip, must be a six digit number
        :param device_id: id of the device to wipe
        :param pin: six digit number (for Intel macOS devices that do not have a T2 chip)"""
        return self.post(f"{device_id}", **kwargs)

    @validate_param_opts(
        [
            ("os_update_mode", ["smart_update", "download_only", "notify_only", "install_asap", "force_update"]),
            ("version_type", ["latest_minor_version", "latest_major_version"]),
        ]
    )
    @api_path_suffix("update_os")
    def update_os(
        self, device_id: str, os_update_mode: Optional[str] = None, version_type: Optional[str] = None, **kwargs
    ) -> Response:
        """Update the OS on a device.
        Note: the 'os_update_mode' parameter is required for macOS devices, it is ignored by iOS/tvOS/iPadOS devices
        :param os_update_mode: optional string indicating the mode to apply to the update; valid options are:
                               'smart_update', 'download_only', 'notify_only', 'install_asap', 'force_update'
        :param version_type: optional string indicating the update version type to apply; valid options are:
                             'latest_minor_version', 'latest_major_version'; the default is 'latest_major_version'"""
        params = {}

        if os_update_mode:
            params["os_update_mode"] = os_update_mode

        if version_type:
            params["version_type"] = version_type

        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("remote_desktop")
    def enable_remote_desktop(self, device_id: str, **kwargs) -> Response:
        """Enable remote desktop on a device (macOS 10.14.4+ only). This only enables Remote Desktop, it does
        not set any of the ARD permission options.
        :param device_id: id of the device to enable Remote Desktop on"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("remote_desktop")
    def disable_remote_desktop(self, device_id: str, **kwargs) -> Response:
        """Disable remote desktop on a device (macOS 10.14.4+ only). This only disables Remote Desktop, it does
        not unset any of the ARD permission options.
        :param device_id: id of the device to enable Remote Desktop on"""
        return self.delete(f"{device_id}", **kwargs)

    @api_path_suffix("bluetooth")
    def enable_bluetooth(self, device_id: str, **kwargs) -> Response:
        """Enable Bluetooth on a device (iOS 11.3+ and macOS 10.13.4+ only).
        :param device_id: id of the device to enable Bluetooth on"""
        return self.post(f"{device_id}", **kwargs)

    @api_path_suffix("bluetooth")
    def disable_bluetooth(self, device_id: str, **kwargs) -> Response:
        """Disable Bluetooth on a device (iOS 11.3+ and macOS 10.13.4+ only).
        :param device_id: id of the device to enable Bluetooth on"""
        return self.delete(f"{device_id}", **kwargs)

    @api_path_suffix("set_time_zone")
    def set_timezone(self, device_id: str, time_zone, **kwargs) -> Response:
        """Set a timezone (using a TZ Identifier value: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
        :param device_id: id of the device to set the TimeZone for
        :param time_zone: string value (TZ Identifier) representing the timezone to set"""
        params = {"time_zone": time_zone}
        return self.post(f"{device_id}", params=params, **kwargs)

    @api_path_suffix("unenroll")
    def unenroll(self, device_id: str, **kwargs) -> Response:
        """Unenroll a device from SimpleMDM.
        :param device_id: id of the device to unenroll"""
        return self.post(f"{device_id}", **kwargs)
