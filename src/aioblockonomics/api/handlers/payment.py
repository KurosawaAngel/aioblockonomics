from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from aiohttp import web

from aioblockonomics import Blockonomics, Payment
from aioblockonomics.enums import PaymentStatus

PaymentHandler = Callable[[Payment, web.Application, Blockonomics], Awaitable[Any]]


@dataclass
class PaymentHandlerObject:
    func: PaymentHandler
    status_filter: PaymentStatus | None = None
    secret_token: str | None = None

    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: Blockonomics
    ) -> Any:
        return await self.func(payment, app, blockonomics)
