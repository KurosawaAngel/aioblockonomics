class BlockonomicsAPIError(Exception):
    """
    This is the base class for all Blockonomics API exceptions.
    """


class InternalServerError(BlockonomicsAPIError):
    """
    This exception is raised when a required parameter is missing or server unavailable.
    """


class UnauthorizedError(BlockonomicsAPIError):
    """
    This exception is raised when the request is unauthorized.
    """


class UnknownError(BlockonomicsAPIError):
    def __init__(self, status_code: int, content: str):
        self.status_code = status_code
        self.content = content

    def __str__(self) -> str:
        return (
            f"Got an unknown error with status code {self.status_code} from Blockonomics API\n"
            f"Content: {self.content}"
        )
