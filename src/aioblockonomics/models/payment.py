from aioblockonomics import PaymentStatus
from aioblockonomics.models import BaseModel


class Payment(BaseModel):
    """
    This is the Payment class which represents HTTP Callback from payment.

    Attributes:
        status (PaymentStatus): The status of the transaction.
                                0 - Unconfirmed, 1 - Partially Confirmed, 2 - Confirmed.
        addr (str): The receiving Bitcoin address.
        value (int): The received payment amount in satoshis.
        txid (str): The ID of the paying transaction.
        rbf (int | None): For unconfirmed transactions, an rbf attribute may be returned.
                          It is optional and may not always be present.
    """

    status: PaymentStatus
    addr: str
    value: int
    txid: str
    rbf: int | None

    @property
    def btc_value(self) -> float:
        return self.value / 1e8

    def convert_to_fiat(self, rate: float) -> float:
        return self.btc_value * rate
