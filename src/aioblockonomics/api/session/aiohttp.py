from typing import Any

import aiohttp

from aioblockonomics.api.session import BaseSession
from aioblockonomics.enums import RequestMethod
from aioblockonomics.urls import BASE_URL


class AiohttpSession(BaseSession):
    """
    This is the aiohttp session which is used to make requests to the Blockonomics API.
    """

    def __init__(self) -> None:
        self._session = None

    async def make_request(
        self,
        method: RequestMethod,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str | int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> str:
        session = self._get_session()

        async with session.request(
            method, url, headers=headers, params=params, data=data
        ) as response:
            response.raise_for_status()
            return await response.text()

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
