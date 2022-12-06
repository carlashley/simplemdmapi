from requests.models import Response
from ..connector import SimpleMDMConnector


class Enrollments(SimpleMDMConnector):
    """Enrollments.

    SimpleMDM API Documentation: https://simplemdm.com/docs/api/#enrollments
    """
    def __init__(self, endpoint: str = "enrollments") -> None:
        self.endpoint = endpoint
        super().__init__()

    def delete(self, enrollment_id: int | str, **kwargs) -> Response:
        """Delete an enrollment.

        :param enrollment_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.delete(url=f"{enrollment_id}", **kwargs)  # Return 204 status

    def list_all(self, **kwargs) -> Response:
        """List all enrollments.

        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.paginate(**kwargs)  # Return list of enrollment objects

    def show(self, enrollment_id: int | str, **kwargs) -> Response:
        """Show details of an enrollment.

        :param enrollment_id: the id value.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        return self.get(url=f"{enrollment_id}", **kwargs)  # Return an enrollment object

    def send_invitation(self, enrollment_id: int | str, contact: str, **kwargs) -> Response:
        """Send an enrollment invitation to an email address or phone number.

        Note, the phone number must be prefixed with a '+' if it is an international phone number.

        :param enrollment_id: the id value.
        :param contact: the email address or phone number to send the invitation to, international numbers
                        must be prefixed with '+'.
        :param kwargs: specific parameters to provide to the underlying requests function."""
        params = self._k2p(self.send_invitation, vals=locals(), ignored_locals=list())
        return self.post(url=f"{enrollment_id}", params=params, **kwargs)  # Return ??
