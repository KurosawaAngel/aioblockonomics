from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar

from aiohttp import web

from aioblockonomics.enums import PaymentStatus
from aioblockonomics.models import Payment

T = TypeVar("T", contravariant=True)


class PaymentHandler(Protocol[T]):
    @abstractmethod
    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: T
    ) -> Any:
        raise NotImplementedError


@dataclass
class PaymentHandlerObject(Generic[T]):
    func: PaymentHandler[T]
    status_filter: PaymentStatus | None = None
    secret_token: str | None = None

    async def __call__(
        self, payment: Payment, app: web.Application, blockonomics: T
    ) -> Any:
        return await self.func(payment, app, blockonomics)
