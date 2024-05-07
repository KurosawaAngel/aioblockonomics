from enum import StrEnum


class BlockonomicsEndpoint(StrEnum):
    NEW_WALLET = "new_address"
    BTC_PRICE = "price"

    MERCHANT_ORDER = "merchant_order/{order_id}"
    MERCHANT_ORDERS = "merchant_orders"
