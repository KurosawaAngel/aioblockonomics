from enum import IntEnum


class PaymentStatus(IntEnum):
    UNCONFIRMED = 0
    PARTIALLY_CONFIRMED = 1
    CONFIRMED = 2


class OrderStatus(IntEnum):
    """
    Attributes:
        PAYMENT_ERROR (-1): This status is set when the paid BTC amount does not match the expected value.
        UNPAID (0): This status is set when the payment has not been made yet.
        IN_PROCESS (1): This status is set when the payment process is ongoing.
        PAID (2): This status is set when the payment has been successfully completed.
    """

    PAYMENT_ERROR = -1
    UNPAID = 0
    IN_PROCESS = 1
    PAID = 2
