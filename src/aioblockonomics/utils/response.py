from http import HTTPStatus
from typing import Any

from msgspec.json import Decoder

from aioblockonomics.api.exceptions import (
    InternalServerError,
    UnauthorizedError,
    UnknownError,
)
from aioblockonomics.models import ServerError

decoder = Decoder(dict[str, Any])
error_decoder = Decoder(ServerError)


def check_response(raw_result: str, status_code: int) -> dict[str, Any]:
    if status_code == HTTPStatus.OK:
        return decoder.decode(raw_result)

    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        error = error_decoder.decode(raw_result)
        raise InternalServerError(error.message)

    if status_code == HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedError("Invalid or expired API token")

    raise UnknownError(status_code, raw_result)
