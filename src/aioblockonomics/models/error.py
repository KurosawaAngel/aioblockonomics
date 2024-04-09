from .base import BaseBlockonomicsModel


class ServerError(BaseBlockonomicsModel):
    """
    Attributes:
        message (str): The error message.
        status (int): Status code.
    """

    status: int
    message: str
