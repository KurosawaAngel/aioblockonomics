import logging

from aiohttp import web

from aioblockonomics import BTCPrice, NewWallet, Payment
from aioblockonomics.api.handlers import PaymentHandler, PaymentHandlerObject
from aioblockonomics.api.session import AiohttpSession, BaseSession
from aioblockonomics.enums import CurrencyCode, PaymentStatus, RequestMethod
from aioblockonomics.urls import PRICE_URL

logger = logging.getLogger(__name__)


class Blockonomics:
    def __init__(
        self,
        api_key: str,
        *,
        session: BaseSession | None = None,
    ):
        self.__headers = {"Authorization": f"Bearer {api_key}"}
        self.session = session or AiohttpSession()
        self._payment_handlers: list[PaymentHandlerObject] = []

    async def get_btc_price(self, currency_code: CurrencyCode) -> BTCPrice:
        response = await self.session.make_request(
            RequestMethod.GET, PRICE_URL, params={"currency": currency_code}
        )
        return BTCPrice.model_validate_json(
            response, context={"currency": currency_code}
        )

    async def create_new_wallet(
        self, reset: int | None, match_account: str | None
    ) -> NewWallet:
        params = {}
        if reset:
            params["reset"] = reset
        if match_account:
            params["match_account"] = match_account

        response = await self.session.make_request(
            RequestMethod.POST, PRICE_URL, params=params, headers=self.__headers
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

    async def get_payment_update(self, request: web.Request) -> web.Response:
        payment = Payment.model_validate_json(await request.json())
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
