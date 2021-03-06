import json

from aiohttp import web, WSMsgType

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.Decorators.authentication import authentication
from src.WS.Response import WSResponse


class WSGetInfo(web.View):
    """A Class used to represent Web View of GetFriends method via WebSocket."""

    @authentication
    async def get(self, token: str) -> web.WebSocketResponse:
        """The function allows you to get information about all users from given ids.

        :param token: Token of current user.
        :type: str

        :return: JSON response with result information.
        :rtype: web.WebSocketResponse
        """
        ws = WSResponse()
        await ws.prepare(self.request)
        self.request.app['logger'].info("User connected in via WebScoket.")
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type != WSMsgType.ERROR:
                self.request.app['logger'].info("WSGetInfo.get called.")
                json_request = json.loads(str(msg.data, encoding='utf-8'))
                api = self.request.app['users'][token]
                try:
                    result = await api.get_info(
                        user_ids=json_request['ids'],
                        fields=json_request['fields']
                    )
                    self.request.app['logger'].info(f"WSGetInfo.get result status code {result['status']}.")
                    await ws.send_json(result)
                except KeyError as e:
                    self.request.app['logger'].error(f"WSGetInfo.get error: {str(e)}.")
                    await ws.send_json(
                        Response(status=ResponseStatus.SERVER_ERROR, reason=str(e), response_type=ResponseTypes.ERROR))

            else:
                self.request.app['logger'].info('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('WS connection closed')

        return ws
