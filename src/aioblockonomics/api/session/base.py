from abc import abstractmethod
from typing import Any, Protocol

from aioblockonomics.enums import RequestMethod


class BaseSession(Protocol):
    @abstractmethod
    async def make_request(
        self,
        method: RequestMethod,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, str | float | int]:
        """
        Asynchronous method to make a request to the Blockonomics API.

        Args:
            method (RequestMethod): The HTTP method to be used for the request.
            url (str): The URL to which the request will be made.
            headers (dict[str, str] | None): Optional; The headers to include in the request.
            params (dict[str, str | int] | None): Optional; The URL parameters to include in the request.
            data (dict[str, Any] | None): Optional; The body data to include in the request.

        Returns:
            dict[str, str | float | int]: The response from the Blockonomics API.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        This method is used to close the aiohttp.ClientSession object.
        """
        raise NotImplementedError
