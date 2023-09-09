from functools import wraps
from pathlib import Path
from typing import Any, Callable

from ._utilities import urljoin


class StatusesMixin:
    def _ignore_status_errs(self, statuses: list[int]) -> list[int]:
        """Generate a list of ignoreable status error codes.
        :param statuses: list of error codes to merge with default ignored status codes"""
        return [*statuses, *self.HTTP_IGNORE_STATUS_ERR]

    def _retry_status_codes(self, statuses: list[int]) -> list[int]:
        """Generate a list of status codes where a retry is performed if an error/timeout occurs.
        :param statuses: list of status codes to merge with default retry status codes"""
        return [*statuses, *self.HTTP_RETRY_STATUS_LIST]


class TokenMixin:
    def token_is_file(self, tkn: str | Path) -> bool:
        """Return True/False if the token is a file object and exists.
        :param tkn: path object"""
        tkn = Path(tkn)
        return tkn.is_file() and tkn.exists()

    def read_token(self, tkn: Path, _mode: str = "rb", _enc: str = "utf-8") -> str:
        """Read the token from a file object.
        :param tkn: path object"""
        if self.token_is_file(tkn):
            with tkn.open(_mode, encoding=_enc) as f:
                return f.read().strip()
        else:
            return tkn.strip()
