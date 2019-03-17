import json
from typing import Optional, Any

from aiohttp.helpers import sentinel
from aiohttp.typedefs import LooseHeaders
from aiohttp.web_response import Response


def json_response(data: Any = sentinel, *,
                  text: str = None,
                  body: bytes = None,
                  status: int = 200,
                  reason: Optional[str] = None,
                  headers: LooseHeaders = None,
                  content_type: str = 'application/json') -> Response:
    if data is not sentinel:
        if text or body:
            raise ValueError(
                "only one of data, text, or body should be specified"
            )
        else:
            text = json.dumps(data, ensure_ascii=False)
    return Response(text=text, body=body, status=status, reason=reason,
                    headers=headers, content_type=content_type)
