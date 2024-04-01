from aioblockonomics.api.session import BaseSession
from aioblockonomics.session import AiohttpSession


class Blockonomics:
    _headers: dict[str, str]
    session: BaseSession

    def __init__(
        self,
        api_key: str,
        *,
        client: BaseSession | None = None,
    ):
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self.client = client or AiohttpSession()
