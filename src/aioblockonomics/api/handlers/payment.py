from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, TYPE_CHECKING

from aiohttp import web

from aioblockonomics.enums import PaymentStatus
from aioblockonomics.models import Payment

if TYPE_CHECKING:
    from aioblockonomics.client import AioBlockonomics


class PaymentHandler(Protocol):
    @abstractmethod
    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: "AioBlockonomics"
    ) -> Any:
        raise NotImplementedError


@dataclass
class PaymentHandlerObject:
    func: PaymentHandler
    status_filter: PaymentStatus | None = None
    secret_token: str | None = None

    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: "AioBlockonomics"
    ) -> Any:
        return await self.func(payment, app, blockonomics)
