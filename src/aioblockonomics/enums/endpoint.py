from enum import StrEnum


class BlockonomicsEndpoint(StrEnum):
    NEW_WALLET = "/api/new_address"
    BTC_PRICE = "/api/price"

    MERCHANT_ORDER = "/api/merchant_order/{order_id}"
    MERCHANT_ORDERS = "/api/merchant_orders"
