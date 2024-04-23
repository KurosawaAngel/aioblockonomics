from http import HTTPStatus
from typing import Any

from msgspec import DecodeError, convert
from msgspec.json import Decoder

from aioblockonomics.api.exceptions import (
    InternalServerError,
    UnauthorizedError,
    UnknownError,
)
from aioblockonomics.models import ServerError

decoder = Decoder(dict[str, Any])


def check_response(raw_result: str, status_code: int) -> dict[str, Any]:
    if status_code == HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedError("Invalid or expired API token")

    try:
        resp = decoder.decode(raw_result)
    except DecodeError:
        raise UnknownError(status_code, raw_result)

    if status_code == HTTPStatus.OK:
        return resp

    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        error = convert(resp, ServerError)
        raise InternalServerError(error.message)

    raise UnknownError(status_code, raw_result)
