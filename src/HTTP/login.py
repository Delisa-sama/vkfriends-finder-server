from aiohttp import web

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.API.vkapirequest import VkAPI


class HTTPLogin(web.View):
    """A Class used to represent Web View of Login method via HTTP."""

    async def post(self) -> web.Response:
        """HTTP Decorators Feature.

        :return: JSON response with result information.
        :rtype: web.Reponse
        """
        data = await self.request.json()
        try:
            vk_api = VkAPI()
            result = await vk_api.auth(
                {
                    'login': data['login'],
                    'password': data['password']
                }
            )
            self.request.app['logger'].error("User logged in via HTTPLogin.")
        except KeyError as e:
            self.request.app['logger'].error("Lack of login or password")
            return web.json_response(
                Response(status=ResponseStatus.SERVER_ERROR, reason=str(e), token='NULL',
                         response_type=ResponseTypes.ERROR))

        if result.is_error():
            self.request.app['logger'].error(result)
            return web.json_response(Response(status=result['status'], reason=result['reason'], token='NULL',
                                              response_type=ResponseTypes.ERROR))

        self.request.app['users'][vk_api.session.access_token] = vk_api
        return web.json_response(Response(status=result['status'], token=vk_api.session.access_token, reason='OK',
                                          response_type=ResponseTypes.AUTH_TOKEN))
