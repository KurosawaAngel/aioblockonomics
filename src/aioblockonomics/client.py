from aiohttp import ClientSession
from dataclass_rest import get, post

from aioblockonomics.api import BASE_URL, BaseClient
from aioblockonomics.enums import (
    CurrencyCode,
)
from aioblockonomics.models import BTCPrice, NewWallet
from aioblockonomics.models.balance import BalanceBody, BalanceResponse


class AioBlockonomics(BaseClient):
    """
    Blockonomics API client.
    Consists of methods to interact with Blockonomics API.

    API DOCUMENTATION: https://www.blockonomics.co/views/api.html
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        session: ClientSession | None = None,
    ) -> None:
        super().__init__(api_key, base_url=base_url, session=session)

    @get("price")
    async def get_btc_price(self, currency: CurrencyCode) -> BTCPrice:
        pass

    @get("new_address")
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
        pass

    @post("balance")
    async def get_balance(self, body: BalanceBody) -> BalanceResponse:
        pass
