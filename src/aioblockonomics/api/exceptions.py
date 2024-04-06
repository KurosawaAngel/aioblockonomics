class BlockonomicsAPIError(Exception):
    """
    This is the base class for all Blockonomics API exceptions.
    """


class InternalServerError(BlockonomicsAPIError):
    """
    This exception is raised when a required parameter is missing.
    """


class UnauthorizedError(BlockonomicsAPIError):
    """
    This exception is raised when the request is unauthorized.
    """


class UnknownError(BlockonomicsAPIError):
    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text

    def __str__(self) -> str:
        return (
            f"Got an unknown error with status code {self.status_code}"
            "from Blockonomics API"
            f"Content: {self.text}"
        )
