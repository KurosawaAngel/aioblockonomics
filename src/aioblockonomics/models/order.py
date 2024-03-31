from aioblockonomics import OrderStatus
from aioblockonomics.models import BaseModel


class Order(BaseModel):
    """
    This is the Order class which represents an order from HTTP callback.

    Attributes:
        status (OrderStatus): The status of the order.
        order_id (str): The unique identifier of the order.
    """

    status: OrderStatus
    order_id: str
