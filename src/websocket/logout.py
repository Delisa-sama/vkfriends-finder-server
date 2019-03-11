from aiohttp import web

from src.Decorators.authentication import authentication


class WSLogout(web.View):
    """A Class used to represent Web View of Logout method via WebSocket."""

    @authentication
    async def get(self, token: str) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        del self.request.app['users'][token]

        await ws.send_json({'status': "OK"})

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('websocket connection closed')
        return ws
