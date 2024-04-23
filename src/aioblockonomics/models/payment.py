import msgspec

from aioblockonomics.enums import PaymentStatus


class Payment(msgspec.Struct, frozen=True, kw_only=True):
    """
    This is the Payment class which represents HTTP Callback from payment.

    Origin: https://www.blockonomics.co/views/api.html#httpcallback

    Attributes:
        status (PaymentStatus): The status of the transaction.
                                0 - Unconfirmed, 1 - Partially Confirmed, 2 - Confirmed.
        addr (str): The receiving Bitcoin address.
        value (int): The received payment amount in satoshi.
        txid (str): The ID of the paying transaction.
        rbf (int | None): For unconfirmed transactions, a rbf attribute may be returned.
        secret (str | None): The secret token for the callbacks.
    """

    status: PaymentStatus
    addr: str
    value: int
    txid: str
    rbf: int | None = None
    secret: str | None = None

    @property
    def btc_value(self) -> float:
        return self.value / 1e8

    def convert_to_fiat(self, rate: float) -> float:
        return self.btc_value * rate
