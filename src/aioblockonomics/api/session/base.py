from abc import ABC, abstractmethod
from http import HTTPMethod
from typing import Any, Mapping

from aioblockonomics.api.url import BLOCKONOMICS_URL
from aioblockonomics.enums import BlockonomicsEndpoint


class BaseSession(ABC):
    """
    Base class for all Session classes.
    """

    def __init__(self, base_url: str = BLOCKONOMICS_URL) -> None:
        self.base_url = base_url

    @abstractmethod
    async def make_request(
        self,
        method: HTTPMethod,
        url: BlockonomicsEndpoint,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> str:
        """
        Asynchronous method to make a request to the Blockonomics API.

        Args:
            method (HTTPMethod): The HTTP method to be used for the request.
            url (str): The URL to which the request will be made.
            headers (dict[str, str] | None): Optional; The headers to include in the request.
            params (dict[str, Any] | None): Optional; The URL parameters to include in the request.
            data (dict[str, Any] | None): Optional; The body data to include in the request.

        Returns:
            str: The JSON response from the Blockonomics API.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        This method is used to close the ClientSession object.
        """
        raise NotImplementedError
