from http import HTTPStatus
from typing import Any

from adaptix import P, Retort, dumper
from aiohttp import ClientResponse, ClientSession
from dataclass_rest.client_protocol import FactoryProtocol
from dataclass_rest.http.aiohttp import AiohttpClient, AiohttpMethod
from dataclass_rest.http_request import HttpRequest

from aioblockonomics.exceptions import (
    InternalServerError,
    UnauthorizedError,
    UnknownError,
)
from aioblockonomics.models.balance import BalanceBody
from aioblockonomics.models.error import ServerError

BASE_URL = "https://www.blockonomics.co/api/"


class BlockonomicsMethod(AiohttpMethod):
    client: "BaseClient"

    async def _on_error_default(self, response: ClientResponse) -> Any:
        if response.status == HTTPStatus.UNAUTHORIZED:
            raise UnauthorizedError("Invalid or expired API token")

        if response.status == HTTPStatus.INTERNAL_SERVER_ERROR:
            json = await response.json()
            error = self.client.response_body_factory.load(json, ServerError)
            raise InternalServerError(error.message)

        raise UnknownError(response.status, await response.text())

    async def _pre_process_request(self, request: HttpRequest) -> HttpRequest:
        request.headers["Authorization"] = f"Bearer {self.client._api_key}"
        request.query_params = {
            k: v for k, v in request.query_params.items() if v is not None
        }
        return request


class BaseClient(AiohttpClient):
    method = BlockonomicsMethod

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        session: ClientSession | None = None,
    ) -> None:
        self._api_key = api_key
        client_session = session or ClientSession()
        super().__init__(base_url=base_url, session=client_session)

    def _init_request_body_factory(self) -> FactoryProtocol:
        return Retort(recipe=(dumper(P[BalanceBody].addr, lambda x: " ".join(x))))
