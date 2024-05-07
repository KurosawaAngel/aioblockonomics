from http import HTTPStatus
from typing import Any

from aiohttp import ClientResponse
from dataclass_rest.http.aiohttp import AiohttpMethod

from aioblockonomics.api.exceptions import (
    InternalServerError,
    UnauthorizedError,
    UnknownError,
)
from aioblockonomics.models.error import ServerError


class APIMethod(AiohttpMethod):
    async def _on_error_default(self, response: ClientResponse) -> Any:
        if response.status == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError("Invalid or expired API token")

        if response.status == HTTPStatus.INTERNAL_SERVER_ERROR:
            json = await response.json()
            error = self.client.response_body_factory.load(json, ServerError)
            raise InternalServerError(error.message)

        raise UnknownError(response.status, await response.text())
