from aioblockonomics.models import BaseModel


class NewAddress(BaseModel):
    """
    This is the NewAddress class which represents a new address in the Blockonomics service.

    Attributes:
        address (str): The new Bitcoin address.
        reset (int | None): Reset index.
        account (str | None): Linked address account.
    """

    address: str
    reset: int | None
    account: str | None
