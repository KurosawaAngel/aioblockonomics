from dataclasses import dataclass
from typing import Awaitable, Callable

from aiohttp import web

from aioblockonomics import Blockonomics, Payment
from aioblockonomics.enums import PaymentStatus


@dataclass
class PaymentHandler:
    func: Callable[[Payment, web.Application, Blockonomics], Awaitable[web.Response]]
    status_filter: PaymentStatus | None = None
    secret_token: str | None = None

    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: Blockonomics
    ) -> web.Response:
        return await self.func(payment, app, blockonomics)
