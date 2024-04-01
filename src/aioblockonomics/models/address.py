from aioblockonomics.models import BaseModel


class NewWallet(BaseModel):
    """
    This is the NewAddress class which represents a new address in the Blockonomics service to accept payments.

    Origin: https://www.blockonomics.co/views/api.html#newaddress

    Attributes:
        address (str): The new Bitcoin address.
        reset (int | None): This will not increment index and will keep giving last generated address.
        account (str | None): Linked address account.
    """

    address: str
    reset: int | None
    account: str | None
