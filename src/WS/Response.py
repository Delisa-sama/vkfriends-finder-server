import json
from typing import Any, Optional

from aiohttp.web_ws import WebSocketResponse


class WSResponse(WebSocketResponse):
    def __init__(self):
        super().__init__()

    async def send_json(self, data: Any, compress: Optional[bool] = None, **kwargs):
        await self.send_str(json.dumps(data, ensure_ascii=False), compress=compress)
