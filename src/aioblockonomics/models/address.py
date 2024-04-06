from .base import BaseBlockonomicsModel


class NewWallet(BaseBlockonomicsModel):
    """
    This is the NewAddress class which represents a new address in the Blockonomics service to accept payments.

    Origin: https://www.blockonomics.co/views/api.html#newaddress

    Attributes:
        address (str): The new Bitcoin address.
        reset (int | None): Reset index.
        account (str | None): Linked address account.
    """

    address: str
    reset: int | None
    account: str | None
