from typing import Any

import aiohttp

from aioblockonomics.enums.method import Method
from aioblockonomics.urls import BASE_URL


class BaseSession:
    """
    This is the BaseSession class which is used as a base for creating sessions with the Blockonomics API.

    Attributes:
        _session (aiohttp.ClientSession | None): An instance of aiohttp.ClientSession or None.
                                                This is used to make HTTP requests to the Blockonomics API.
        api_key (str): The API key provided by Blockonomics for accessing their API.
    """

    _session: aiohttp.ClientSession | None
    api_key: str

    __slots__ = ("_session", "api_key", "headers")

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._session = None
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def make_request(self, method: Method, url: str, **kwargs) -> dict[str, Any]:
        """
        This method is used to make a request to the Blockonomics API.

        Args:
            method (str): The HTTP method to be used for the request.
            url (str): The URL to which the request will be made.
            **kwargs: Additional keyword arguments to be passed to the aiohttp.ClientSession.request method.
        """
        session = self.get_session()

        async with session.request(method, url, **kwargs) as response:
            return await response.json()

    async def close(self) -> None:
        """
        This method is used to close the aiohttp.ClientSession object.
        """
        if self._session is not None:
            await self._session.close()

    def get_session(self) -> aiohttp.ClientSession:
        """
        This method is used to get the aiohttp.ClientSession object.

        Returns:
            aiohttp.ClientSession: The aiohttp.ClientSession object.
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(BASE_URL, headers=self.headers)
        return self._session
