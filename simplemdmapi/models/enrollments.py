from ..api import SimpleMDMConnector
from ..typehints import OptionalDict, UnionIntString
from typing import Any


class Enrollments(SimpleMDMConnector):
    """Enrollments.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#enrollments
    """
    def __init__(self, endpoint: str = "enrollments") -> None:
        self.endpoint = endpoint
        super().__init__()

    def delete(self, enrollment_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Delete an enrollment.

        :param enrollment_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{enrollment_id}", params=params, **kwargs)  # Return 204 status

    def list_all(self, params: OptionalDict = dict(), **kwargs) -> Any:
        """List all enrollments.

        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(params=params, **kwargs)  # Return list of enrollment objects

    def show(self, enrollment_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Show details of an enrollment.

        :param enrollment_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{enrollment_id}", params=params, **kwargs)  # Return an enrollment object

    def send_invitation(self, enrollment_id: UnionIntString, params: OptionalDict = dict(), **kwargs) -> Any:
        """Send an enrollment invitation to an email address or phone number.

        Note, the phone number must be prefixed with a '+' if it is an international phone number.

        :param enrollment_id: the id value.
        :param params: specific parameters to provide to the API query.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        kwargs["required_params"] = ["contact"]
        kwargs["validate_params"] = ["contact"]

        return self.post(url=f"{enrollment_id}", params=params, **kwargs)  # Return ??
