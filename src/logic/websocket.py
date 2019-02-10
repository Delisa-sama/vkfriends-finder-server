import json

from aiohttp import web, WSMsgType, log

from src.auth.user import User, pool as users
from src.logic.vkapirequest import VKAPIRequest


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)

                if json_request['action'] == 'close':
                    await ws.close()

                elif json_request['action'] == 'login':
                    user = User(data=json_request['data'])
                    result = await user.vk_auth()
                    if result['status'] == 'ERROR':
                        await ws.send_json(data=result)
                    else:
                        users[user.vk_session.access_token] = user
                        await ws.send_json({'status': result['status'], 'token': user.vk_session.access_token})

                    log.server_logger.debug(result)

                elif json_request['action'] == 'get_friends':
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
