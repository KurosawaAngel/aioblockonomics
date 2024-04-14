from abc import abstractmethod
from http import HTTPMethod
from typing import Any, Mapping, Protocol

from aioblockonomics.enums import BlockonomicsEndpoint


class BaseSession(Protocol):
    """
    Base class for all Session classes.
    """

    base_url: str

    @abstractmethod
    async def make_request(
        self,
        method: HTTPMethod,
        url: BlockonomicsEndpoint,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, int | str] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Asynchronous method to make a request to the Blockonomics API.

        Args:
            method (HTTPMethod): The HTTP method to be used for the request.
            url (str): The URL to which the request will be made.
            headers (dict[str, str] | None): Optional; The headers to include in the request.
            params (dict[str, Any] | None): Optional; The URL parameters to include in the request.
            data (dict[str, Any] | None): Optional; The body data to include in the request.

        Returns:
            dict[str, Any]: The JSON response from the Blockonomics API.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        This method is used to close the ClientSession object.
        """
        raise NotImplementedError
