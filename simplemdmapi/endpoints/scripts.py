from requests.models import Response
from typing import Generator

from ..connector import SimpleMDMConnector
from .._decorators import file_upload, paginate, param_kwargs, url_suffixes
from .._validators import all_params, any_params, bad_combo_params, validate_param_opts

_param_kwargs = {
    "scripts.list_all": [
        "starting_after",
        "limit",
    ],
    "scripts.create": ["name", "variable_support", "file"],
    "script_jobs.list_all": [
        "starting_after",
        "limit",
    ],
    "script_jobs.create": [
        "script_id",
        "device_ids",
        "group_ids",
        "assignment_group_ids",
        "custom_attribute",
        "custom_attribute_regex",
    ],
}

_param_opts_validation = {
    "scripts.update": [
        ("deploy_to", ["all", "none", "outdated"]),
    ],
    "managed_script.create": [
        (
            "value_type",
            ["boolean", "date", "float", "float array", "integer", "integer array", "string", "string array"],
        ),
    ],
}


class Scripts(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#scripts"""

    def __init__(self, endpoint: str = "scripts", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @param_kwargs(_param_kwargs["scripts.list_all"])
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all scripts.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: script id to start pagination after; default is 0 for first script"""
        return self.get(**kwargs)

    def retrieve(self, script_id: str, **kwargs) -> Response:
        """Retrieve one script.
        :param script_id: id of the script"""
        return self.get(f"{script_id}", **kwargs)

    @all_params(["name", "file"])
    @any_params(_param_kwargs["scripts.create"])
    @param_kwargs(_param_kwargs["scripts.create"])
    @file_upload("file")
    def create(self, **kwargs) -> Response:
        """Add a new script.
        :param file: string representation of the file path to upload, first line must contain a valid shebang, such
                     as '#!/bin/sh'
        :param name: required, name of the script (this is how it is listed in the Admin UI)
        :param variable_support: optional, enable or disable variable support in the script, use '1' to enable,
                                 '0' to disable"""
        return self.post(**kwargs)

    @any_params(_param_kwargs["scripts.create"])
    @param_kwargs(_param_kwargs["scripts.create"])
    @file_upload("file")
    def update(self, script_id: str, **kwargs) -> Response:
        """Update an existing script.
        :param script_id: id of the script
        :param file: string representation of the file path to upload, first line must contain a valid shebang, such
                     as '#!/bin/sh'
        :param name: required, name of the script (this is how it is listed in the Admin UI)
        :param variable_support: optional, enable or disable variable support in the script, use '1' to enable,
                                 '0' to disable"""
        return self.patch(f"{script_id}", **kwargs)

    def remove(self, script_id: str, **kwargs) -> Response:
        """Delete a script.
        :param script_id: id of the script"""
        return self.delete(f"{script_id}", **kwargs)


class ScriptJobs(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#script-jobs"""

    def __init__(self, endpoint: str = "script_jobs", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @param_kwargs(_param_kwargs["script_jobs.list_all"])
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all script jobs.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: script id to start pagination after; default is 0 for first script"""
        return self.get(**kwargs)

    def retrieve(self, job_id: str, **kwargs) -> Response:
        """Retrieve one script job.
        :param job_id: id of the script job"""
        return self.get(f"{job_id}", **kwargs)

    @all_params(["script_id"])
    @any_params(["device_ids", "group_ids", "assignment_group_ids"])
    @param_kwargs(_param_kwargs["cscript_jobs.reate"])
    def create(self, **kwargs) -> Response:
        """Add a new script job.
        :param script_id: required, id of the script to run on devices
        :param device_ids: comma separated list of device ids to run the script on
        :param group_ids: comma seprarted list of group ids to run the script on, any macOS device in the group/s
                          will be included in the script job
        :param assignment_group_ids: comma separated list of assignment group ids to run the script on, any macOS
                                     device in the assignment group/s will be included in the script job
        :param custom_attribute: optional, output for the script will be stored in this custom attribute on each
                                 device
        :param custom_attribute_regex: optional, used to sanitize output from the script before storing it in
                                       the custom attribute, can be left empty but '\n' is recommended"""
        kwargs.setdefault("custom_attribute_regex", "\n")
        return self.post(**kwargs)

    def cancel(self, job_id: str, **kwargs) -> Response:
        """Cancel a script job.
        :param job_id: id of the script job"""
        return self.delete(f"{job_id}", **kwargs)
