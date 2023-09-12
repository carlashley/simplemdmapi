from requests.models import Response
from typing import Generator

from ..connector import SimpleMDMConnector
from .._decorators import paginate, param_kwargs, url_suffixes
from ..validators import all_params

_param_kwargs = {
    "list_all": [
        "starting_after",
        "limit",
    ],
    "send_invitations": ["contact"],
}

_param_opts_validation = {}


class Enrollments(SimpleMDMConnector):
    """SimpleMDM API Documentation: https://simplemdm.com/docs/api/#enrollments"""

    def __init__(self, endpoint: str = "enrollments", dry_run: bool = False) -> None:
        self.endpoint = endpoint
        self.dry_run = dry_run
        super().__init__()

    @param_kwargs(_param_kwargs["list_all"])
    @paginate
    def list_all(self, **kwargs) -> Generator[dict, None, None]:
        """List all enrollments.
        :param limit: number of objects per page; default is 100 (the SimpleMDM API returns 10 objects by default)
        :param starting_after: group id to start pagination after; default is 0 for first device"""
        return self.get(**kwargs)

    def show(self, enr_id: str, **kwargs) -> Response:
        """Retrieve one device.
        :param enr_id: id of the enrollment"""
        return self.get(enr_id, **kwargs)

    @all_params(_param_kwargs["send_invitations"])
    @param_kwargs(_param_kwargs["send_invitations"])
    @url_suffixes("invitations")
    def send_invitations(self, enr_id: str, **kwargs) -> Response:
        """Clone a group group.
        :param enr_id: id of the enrollment
        :param contact: required, email or phone number to send in the invitations"""
        return self.post(enr_id, **kwargs)

    def delete(self, **kwargs) -> Response:
        """Delete enrollments."""
        return self.delete(**kwargs)
