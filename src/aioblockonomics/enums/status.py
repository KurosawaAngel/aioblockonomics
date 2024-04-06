from enum import IntEnum


class PaymentStatus(IntEnum):
    UNCONFIRMED = 0
    PARTIALLY_CONFIRMED = 1
    CONFIRMED = 2


class OrderStatus(IntEnum):
    """
    Attributes:
        PAYMENT_ERROR (-1): Paid BTC amount does not match the expected value.
        UNPAID (0): Payment has not been made yet.
        IN_PROCESS (1): Payment process is ongoing.
        PAID (2): Payment has been successfully completed.
    """

    PAYMENT_ERROR = -1
    UNPAID = 0
    IN_PROCESS = 1
    PAID = 2
