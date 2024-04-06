from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol

from aiohttp import web

from aioblockonomics import Blockonomics, Payment
from aioblockonomics.enums import PaymentStatus


class PaymentHandler(Protocol):
    @abstractmethod
    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: Blockonomics
    ) -> Any:
        raise NotImplementedError


@dataclass
class PaymentHandlerObject:
    func: PaymentHandler
    status_filter: PaymentStatus | None = None
    secret_token: str | None = None

    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: Blockonomics
    ) -> Any:
        return await self.func(payment, app, blockonomics)
