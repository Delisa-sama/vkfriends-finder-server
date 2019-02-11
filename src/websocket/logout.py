from aiohttp import web

from src.Authentication.decorator import authentication


class WSLogout(web.View):
    @authentication
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        await ws.send_json({'status': "OK"})

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('websocket connection closed')
        return ws