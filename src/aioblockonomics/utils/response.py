from http import HTTPStatus

from aioblockonomics.api.exceptions import (
    InternalServerError,
    UnauthorizedError,
    UnknownError,
)
from aioblockonomics.models import ServerError


def check_response(raw_result: str, status_code: int) -> str:
    if status_code == HTTPStatus.OK:
        return raw_result

    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        error = ServerError.model_validate_json(raw_result)
        raise InternalServerError(error.message)

    if status_code == HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedError("Invalid or expired API token")

    raise UnknownError(status_code, raw_result)
