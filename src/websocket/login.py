import json

from aiohttp import web, WSMsgType, log

from src.API.user import User, pool as users


class WSLogin(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)

                user = User(data=json_request['data'])
                result = await user.vk_auth()
                if result['status'] == 'ERROR':
                    await ws.send_json(data=result)
                else:
                    users[user.vk_session.access_token] = user
                    await ws.send_json({'status': result['status'], 'token': user.vk_session.access_token})

                log.server_logger.debug(result)

            elif msg.type == WSMsgType.ERROR:
                log.server_logger.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        log.server_logger.debug('websocket connection closed')

        return ws
