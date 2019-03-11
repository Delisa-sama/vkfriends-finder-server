import json

from aiohttp import web, WSMsgType

from src.API.vkapirequest import get_info
from src.Decorators.authentication import authentication


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
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                json_request = json.loads(msg.data)
                result = await get_info(
                    api=self.request.app['users'][token].vk_api,
                    user_ids=json_request['ids']
                )
                self.request.app['logger'].info("WSGetInfo.get called.")
                await ws.send_json(result)

            elif msg.type == WSMsgType.ERROR:
                self.request.app['logger'].info('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('websocket connection closed')

        return ws
