import json

from aiohttp import web, WSMsgType, log
from aiohttp_session import get_session

from src.auth.user import User


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)  # TODO: check user session

        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)
                if json_request['action'] == 'close':
                    await ws.close()
                elif json_request['action'] == 'login':
                    # TODO: add user to session
                    user = User(data=json_request['data'])
                    result = await user.vk_auth()
                    if result['status'] == 'ERROR':
                        await ws.send_json(data=result)
                    log.server_logger.debug(result)

            elif msg.type == WSMsgType.ERROR:
                log.server_logger.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        log.server_logger.debug('websocket connection closed')

        return ws
