from aioblockonomics import CurrencyCode
from aioblockonomics.models import BaseModel


class BTCPrice(BaseModel):
    """
    This is the BTCPrice class which represents the price of Bitcoin in a specific currency.

    Attributes:
        price (float | None): The price of Bitcoin in the specified currency. None if the price is not available.
        currency (CurrencyCode): The currency in which the price is represented.
    """

    price: float | None
    currency: CurrencyCode
