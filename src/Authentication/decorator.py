from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

from aiohttp import web

from src.API.user import pool as users


def authentication(func):
    async def wrapper(view: web.View):
        qs = urlparse(str(view.request.url))
        query_params = parse_qs(qs.query)
        token = query_params['token'][0]

        if token in users:
            ws = await func(view, token)
        else:
            ws = web.WebSocketResponse()
            await ws.prepare(view.request)
            await ws.send_json({'status': HTTPStatus.UNAUTHORIZED,
                                'reason': "Not authenticated token, login please."})
        return ws

    return wrapper
