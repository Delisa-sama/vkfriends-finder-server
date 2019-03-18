import base64
import json

from aiohttp import web, WSMsgType

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.API.vkapirequest import VkAPI
from src.WS.Response import WSResponse


class WSLogin(web.View):
    """A Class used to represent Web View of Login method via WebSocket."""

    async def get(self) -> web.WebSocketResponse:
        """HTTP Decorators Feature.

        :return: JSON response with result information.
        :rtype: web.WebSocketResponse
        """
        ws = WSResponse()
        await ws.prepare(self.request)
        self.request.app['logger'].info("User connected in via WebScoket.")
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type != WSMsgType.ERROR:
                json_request = json.loads(str(msg.data, encoding='utf-8'))
                print(json_request)
                try:
                    password = str(base64.b64decode(bytes(json_request.get('password'), 'utf-8')), encoding='utf-8')
                    print(password)
                    vk_api = VkAPI()
                    result = await vk_api.auth(
                        {
                            'login': json_request['login'],
                            'password': password
                        }
                    )
                    if result.is_error():
                        self.request.app['logger'].error(result)
                        await ws.send_json(data=result)
                    else:
                        self.request.app['users'][vk_api.session.access_token] = vk_api
                        self.request.app['logger'].error("User logged in via WebScoket.")
                        await ws.send_json({'status': result['status'], 'token': vk_api.session.access_token})
                except KeyError as e:
                    self.request.app['logger'].error(f"WSLogin.get error: {str(e)}.")
                    await ws.send_json(
                        Response(status=ResponseStatus.SERVER_ERROR, reason=str(e), response_type=ResponseTypes.ERROR))

            else:
                self.request.app['logger'].error('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('WS connection closed')

        return ws
