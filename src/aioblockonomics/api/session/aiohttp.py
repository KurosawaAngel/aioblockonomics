from http import HTTPMethod
from typing import Any, Mapping

import aiohttp

from aioblockonomics.api.session.base import BaseSession
from aioblockonomics.api.url import BLOCKONOMICS_URL
from aioblockonomics.enums import BlockonomicsEndpoint
from aioblockonomics.utils import check_response


class AiohttpSession(BaseSession):
    """
    This is the aiohttp session which is used to make requests to the Blockonomics API.
    """

    _session: aiohttp.ClientSession | None

    def __init__(self, base_url: str = BLOCKONOMICS_URL) -> None:
        self._session = None
        self.base_url = base_url

    async def make_request(
        self,
        method: HTTPMethod,
        endpoint: BlockonomicsEndpoint,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> str:
        session = self._get_session()

        async with session.request(
            method, endpoint, headers=headers, params=params, data=data
        ) as response:
            text = await response.text()

        return check_response(text, response.status)

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
            self._session = aiohttp.ClientSession(self.base_url)
        return self._session
