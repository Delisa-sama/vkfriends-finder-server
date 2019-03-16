import json

from aiohttp import web, WSMsgType

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.API.vkapirequest import get_friends, get_info, get_profileinfo
from src.Decorators.authentication import authentication


class WSGetFriends(web.View):
    """A Class used to represent Web View of GetFriends method via WebSocket."""

    @authentication
    async def get(self, token: str) -> web.WebSocketResponse:
        """The function allows you to get information about all the friends of a given user.

        :param token: Token of current user.
        :type: str

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
                    self.request.app['logger'].info(f"WSGetFriends.get called with params: \n"
                                                    f"target_id: {json_request['id']}, \n"
                                                    f"fields: {json_request['fields']}.")
                    api = self.request.app['users'][token].vk_api
                    result = await get_friends(
                        api=api,
                        target_id=json_request['id'],
                        fields=json_request['fields'] if 'fields' in json_request else ''
                    )
                    result['self'] = await get_profileinfo(api=api) if json_request['id'] == 0 else await get_info(
                        api=api,
                        user_ids=[json_request['id']],
                        fields=json_request['fields']
                    )
                    self.request.app['logger'].info(f"WSGetFriends.get result status code {result['status']}.")
                    await ws.send_json(result)
                except KeyError as e:
                    self.request.app['logger'].error(f"WSGetFriends.get error: {str(e)}.")
                    await ws.send_json(
                        Response(status=ResponseStatus.SERVER_ERROR, reason=str(e), response_type=ResponseTypes.ERROR))

            elif msg.type == WSMsgType.ERROR:
                self.request.app['logger'].info('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        self.request.app['logger'].info('WS connection closed')

        return ws
