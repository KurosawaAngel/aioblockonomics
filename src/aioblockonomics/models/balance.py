from dataclasses import dataclass


@dataclass
class BalanceBody:
    addr: list[str]


@dataclass
class Balance:
    addr: str
    confirmed: int
    unconfirmed: int


@dataclass(slots=True)
class BalanceResponse:
    response: list[Balance]
