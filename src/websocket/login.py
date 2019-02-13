import json

from aiohttp import web, WSMsgType

from src.API.user import User


class WSLogin(web.View):
    """A Class used to represent Web View of Login method via WebSocket."""

    async def get(self) -> web.WebSocketResponse:
        """HTTP Authentication Feature.

        :return: JSON response with result information.
        :rtype: web.WebSocketResponse
        """
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)

                user = User()
                result = await user.auth(login=json_request['login'], password=json_request['password'])
                if result['status'] == 'ERROR':
                    self.request.app['logger'].error(result)
                    await ws.send_json(data=result)
                else:
                    self.request.app['users'][user.vk_session.access_token] = user
                    await ws.send_json({'status': result['status'], 'token': user.vk_session.access_token})

                    self.request.app['logger'].info(result)

            elif msg.type == WSMsgType.ERROR:
                self.request.app['logger'].error('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('websocket connection closed')

        return ws
