from typing import Any

import aiohttp

from aioblockonomics.api.protocols import BaseSession
from aioblockonomics.enums import RequestMethod
from aioblockonomics.urls import BASE_URL


class AiohttpSession(BaseSession):
    """
    This is the Session class which is used as a protocols for creating sessions with the Blockonomics API.

    Attributes:
        _session (aiohttp.ClientSession | None): An instance of aiohttp.ClientSession or None.
                                                This is used to make HTTP requests to the Blockonomics API.
    """

    _session: aiohttp.ClientSession | None

    def __init__(self) -> None:
        self._session = None

    async def make_request(
        self,
        method: RequestMethod,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, str | float | int]:
        session = self._get_session()

        async with session.request(
            method, url, headers=headers, params=params, data=data
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    def _get_session(self) -> aiohttp.ClientSession:
        """
        This method is used to get the aiohttp.ClientSession object.
        Base url is set to the Blockonomics API URL.

        Returns:
            aiohttp.ClientSession: The aiohttp.ClientSession object.
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(BASE_URL)
        return self._session

    __call__ = make_request
