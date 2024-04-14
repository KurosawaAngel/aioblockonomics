import msgspec


class BTCPrice(msgspec.Struct, frozen=True, kw_only=True):
    """
    This is the BTCPrice class which represents the price of Bitcoin in a specific currency.

    Attributes:
        price (float | None): The price of Bitcoin in the specified currency. None if the price is not available.
    """

    price: float | None
