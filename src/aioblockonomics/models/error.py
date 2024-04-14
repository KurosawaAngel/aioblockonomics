import msgspec


class ServerError(msgspec.Struct, frozen=True, kw_only=True):
    """
    Attributes:
        message (str): The error message.
        status (int): Status code.
    """

    status: int
    message: str
