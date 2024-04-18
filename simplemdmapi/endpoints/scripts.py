from pathlib import Path
from requests.models import Response
from typing import Generator, Optional

from .. import SimpleMDMConnector
from ..decorators import method_params, paginate


class Scripts(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#scripts"""

    def __init__(self, endpoint: str = "scripts", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
            "create": {
                "all_params": ["name", "variable_support", "file"],
                "req_params": ["file", "name"],
                "file_param": "file",
                "validate": {
                    "variable_support": ["0", "1", 0, 1],
                },
            },
            "update": {
                "all_params": ["name", "variable_support", "file"],
                "req_params": ["file", "name"],
                "file_param": "file",
                "validate": {
                    "variable_support": ["0", "1", 0, 1],
                },
            },
        }

    @method_params
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all scripts.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: script id to start pagination after; default is 0 for first script"""
        return self.get(**kwargs)

    def retrieve(self, script_id: str, **kwargs) -> Response:
        """Retrieve one script.
        :param script_id: id of the script"""
        return self.get(script_id, **kwargs)

    @method_params
    def create(self, **kwargs) -> Response:
        """Add a new script.
        :param file: string representation of the file path to upload, first line must contain a valid shebang, such
                     as '#!/bin/sh'
        :param name: required, name of the script (this is how it is listed in the Admin UI)
        :param variable_support: optional, enable or disable variable support in the script, use '1' to enable,
                                 '0' to disable"""
        return self.post(**kwargs)

    @method_params
    def update(self, script_id: str, **kwargs) -> Response:
        """Update an existing script.
        :param script_id: id of the script
        :param file: string representation of the file path to upload, first line must contain a valid shebang, such
                     as '#!/bin/sh'
        :param name: required, name of the script (this is how it is listed in the Admin UI)
        :param variable_support: optional, enable or disable variable support in the script, use '1' to enable,
                                 '0' to disable"""
        return self.patch(script_id, **kwargs)

    def remove(self, script_id: str, **kwargs) -> Response:
        """Delete a script.
        :param script_id: id of the script"""
        return self.delete(script_id, **kwargs)


class ScriptJobs(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#script-jobs"""

    def __init__(self, endpoint: str = "script_jobs", dry_run: bool = False, tkn: Optional[str | Path] = None) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__(tkn=tkn)

        self._method_kwargs = {
            "list_all": {
                "all_params": ["limit", "starting_after"],
            },
            "create": {
                "all_params": [
                    "script_id",
                    "device_ids",
                    "group_ids",
                    "assignment_group_ids",
                    "custom_attribute",
                    "custom_attribute_regex",
                ],
                "req_params": ["script_id"],
                "any_params": ["device_ids", "group_ids", "assignment_group_ids"],
            },
        }

    @method_params
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all script jobs.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: script id to start pagination after; default is 0 for first script"""
        return self.get(**kwargs)

    def retrieve(self, job_id: str, **kwargs) -> Response:
        """Retrieve one script job.
        :param job_id: id of the script job"""
        return self.get(job_id, **kwargs)

    @method_params
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
        return self.delete(job_id, **kwargs)
