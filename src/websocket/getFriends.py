import json

from aiohttp import web, WSMsgType

from src.API.vkapirequest import VKAPIRequest
from src.Authentication.decorator import authentication


class WSGetFriends(web.View):
    @authentication
    async def get(self, token):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)

                result = await VKAPIRequest().get_friends(
                    user=self.request.app['users'][token],
                    id=json_request['id']
                )

                await ws.send_json(result)

            elif msg.type == WSMsgType.ERROR:
                self.request.app['logger'].info('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('websocket connection closed')

        return ws
