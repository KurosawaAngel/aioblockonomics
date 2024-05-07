import logging

from adaptix import Retort, name_mapping
from aiohttp import ClientSession, web
from dataclass_rest import get
from dataclass_rest.client_protocol import FactoryProtocol
from dataclass_rest.http.aiohttp import AiohttpClient

from aioblockonomics.api.handlers import PaymentHandler, PaymentHandlerObject
from aioblockonomics.api.method import APIMethod
from aioblockonomics.enums import (
    BlockonomicsEndpoint,
    CurrencyCode,
    PaymentStatus,
)
from aioblockonomics.models import BTCPrice, NewWallet, Payment

logger = logging.getLogger(__name__)


class AioBlockonomics(AiohttpClient):
    """
    Blockonomics API client.
    Consists of methods to interact with Blockonomics API.

    API DOCUMENTATION: https://www.blockonomics.co/views/api.html
    """

    method_class = APIMethod

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://www.blockonomics.co/api/",
    ) -> None:
        session = ClientSession(headers={"Authorization": f"Bearer {api_key}"})
        super().__init__(base_url=base_url, session=session)
        self._payment_handlers: list[PaymentHandlerObject] = []

    def _init_request_args_factory(self) -> FactoryProtocol:
        return Retort(recipe=[name_mapping(omit_default=True)])

    async def get_btc_price(self, currency: CurrencyCode) -> float | None:
        """
        Args:
            currency (CurrencyCode): specified currency

        Returns:
            float | None: The price of Bitcoin in the specified currency or None if the price is not available.
        """
        res = await self._get_btc_price(currency)
        return res.price

    @get(BlockonomicsEndpoint.BTC_PRICE)
    async def _get_btc_price(self, currency: CurrencyCode) -> BTCPrice:
        pass

    @get(BlockonomicsEndpoint.NEW_WALLET)
    async def create_new_wallet(
        self,
        *,
        reset: int | None = None,
        match_account: str | None = None,
    ) -> NewWallet:
        """
        Create a new wallet.

        Kwargs:
            reset (int | None): Reset index.
            match_account (str | None): Linked address account.

        Returns:
            NewWallet: The newly created wallet.
        """

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
        payment = self.request_body_factory.load(request.query, Payment)

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
