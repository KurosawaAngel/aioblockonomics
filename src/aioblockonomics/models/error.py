from dataclasses import dataclass


@dataclass(slots=True)
class ServerError:
    """
    Attributes:
        message (str): The error message.
        status (int): Status code.
    """

    status: int
    message: str
