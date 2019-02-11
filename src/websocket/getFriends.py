import json

from aiohttp import web, WSMsgType, log

from src.API.user import pool as users
from src.API.vkapirequest import VKAPIRequest


class WSGetFriends(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)

                token = json_request['token']
                if token not in users:
                    await ws.send_json({'status': 'ERROR', 'exception': 'Token not found'})
                else:
                    request = VKAPIRequest()
                    result = await request.get_friends(user=users[token], id=json_request['id'])
                    await ws.send_json(result)

            elif msg.type == WSMsgType.ERROR:
                log.server_logger.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        log.server_logger.debug('websocket connection closed')

        return ws
