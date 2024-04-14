from http import HTTPStatus
from typing import Any

import msgspec

from aioblockonomics.api.exceptions import (
    InternalServerError,
    UnauthorizedError,
    UnknownError,
)
from aioblockonomics.models import ServerError


def check_response(raw_result: str, status_code: int) -> dict[str, Any]:
    if status_code == HTTPStatus.OK:
        return msgspec.json.decode(raw_result)

    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        error = msgspec.json.decode(raw_result, type=ServerError)
        raise InternalServerError(error.message)

    if status_code == HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedError("Invalid or expired API token")

    raise UnknownError(status_code, raw_result)
