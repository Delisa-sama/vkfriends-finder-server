import json

from aiohttp import web, WSMsgType

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.API.user import User


class WSLogin(web.View):
    """A Class used to represent Web View of Login method via WebSocket."""

    async def get(self) -> web.WebSocketResponse:
        """HTTP Decorators Feature.

        :return: JSON response with result information.
        :rtype: web.WebSocketResponse
        """
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.BINARY:
                json_request = json.loads(str(msg.data, encoding='utf-8'))
                try:
                    user = User()
                    result = await user.auth(login=json_request['login'], password=json_request['password'])
                    if result.is_error():
                        self.request.app['logger'].error(result)
                        await ws.send_json(data=result)
                    else:
                        self.request.app['users'][user.vk_session.access_token] = user

                        self.request.app['logger'].error("User logged in via WebScoket.")

                        await ws.send_json({'status': result['status'], 'token': user.vk_session.access_token})
                except KeyError as e:
                    self.request.app['logger'].error(f"WSLogin.get error: {str(e)}.")
                    await ws.send_json(
                        Response(status=ResponseStatus.SERVER_ERROR, reason=str(e), response_type=ResponseTypes.ERROR))

            elif msg.type == WSMsgType.ERROR:
                self.request.app['logger'].error('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('WS connection closed')

        return ws
