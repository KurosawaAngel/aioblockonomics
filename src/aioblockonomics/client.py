import logging
from http import HTTPMethod

from aiohttp import web

from aioblockonomics.api.handlers import PaymentHandler, PaymentHandlerObject
from aioblockonomics.api.session import AiohttpSession
from aioblockonomics.api.session.base import BaseSession
from aioblockonomics.enums import (
    BlockonomicsEndpoint,
    CurrencyCode,
    PaymentStatus,
)
from aioblockonomics.models import BTCPrice, NewWallet, Payment

logger = logging.getLogger(__name__)


class AioBlockonomics:
    """
    Blockonomics API client.
    Consists of methods to interact with Blockonomics API.

    API DOCUMENTATION: https://www.blockonomics.co/views/api.html
    """

    def __init__(
        self,
        api_key: str,
        *,
        session: BaseSession | None = None,
    ) -> None:
        self.session = session or AiohttpSession()
        self._payment_handlers: list[PaymentHandlerObject] = []
        self.__headers = {"Authorization": f"Bearer {api_key}"}

    async def get_btc_price(self, currency_code: CurrencyCode) -> BTCPrice:
        response = await self.session.make_request(
            HTTPMethod.GET,
            BlockonomicsEndpoint.BTC_PRICE,
            params={"currency": currency_code},
        )
        return BTCPrice.model_validate_json(response)

    async def create_new_wallet(
        self, reset: int | None, match_account: str | None
    ) -> NewWallet:
        param: dict[str, str | int] = {}
        if reset:
            param["reset"] = reset
        if match_account:
            param["match_account"] = match_account

        response = await self.session.make_request(
            HTTPMethod.POST,
            BlockonomicsEndpoint.NEW_WALLET,
            params=param,
            headers=self.__headers,
        )
        return NewWallet.model_validate_json(response)

    def register_payment_handler(
        self,
        func: PaymentHandler,
        secret_token: str | None = None,
        status_filter: PaymentStatus | None = None,
    ):
        handler = PaymentHandlerObject(
            func=func, secret_token=secret_token, status_filter=status_filter
        )
        self._payment_handlers.append(handler)

    async def handle_payment_updates(self, request: web.Request) -> web.Response:
        payment = Payment.model_validate_json(await request.text())

        for handler in self._payment_handlers:
            if handler.status_filter and payment.status != handler.status_filter:
                continue
            if handler.secret_token and payment.secret != handler.secret_token:
                logger.warning(
                    "Secret token mismatch, got [%s] instead [%s]",
                    payment.secret,
                    handler.secret_token,
                )
                continue
            await handler(payment, request.app, self)
        return web.Response(text="ok")
