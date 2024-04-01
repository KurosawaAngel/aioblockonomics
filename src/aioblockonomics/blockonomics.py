from aioblockonomics import BTCPrice, NewWallet
from aioblockonomics.api.session import AiohttpSession, BaseSession
from aioblockonomics.enums import CurrencyCode, RequestMethod
from aioblockonomics.urls import PRICE_URL


class Blockonomics:
    __headers: dict[str, str]
    session: BaseSession

    def __init__(
        self,
        api_key: str,
        *,
        session: BaseSession | None = None,
    ):
        self.__headers = {"Authorization": f"Bearer {api_key}"}
        self.client = session or AiohttpSession()

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
            params["account"] = match_account

        response = await self.session.make_request(
            RequestMethod.POST, PRICE_URL, params=params, headers=self.__headers
        )
        return NewWallet.model_validate_json(response)
