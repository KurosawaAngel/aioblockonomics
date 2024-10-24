from dataclasses import dataclass

from aioblockonomics.enums import OrderStatus


@dataclass(slots=True)
class Order:
    """
    This is the Order class which represents an order from HTTP callback.

    Origin: https://www.blockonomics.co/views/api.html#paymentbuttons

    Attributes:
        status (OrderStatus): The status of the order.
        order_id (str): The unique identifier of the order.
        secret (str | None): The secret for the callbacks.
    """

    status: OrderStatus
    order_id: str
    secret: str | None = None
