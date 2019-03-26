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
            credentials = {
                'login': data['login'],
                'password': data['password']
            }
            self.request.app['logger'].info(credentials)
            result = await vk_api.auth(credentials=credentials)
            self.request.app['users'][vk_api.session.access_token] = vk_api
            self.request.app['logger'].info("User logged in via HTTPLogin.")
        except KeyError as e:
            self.request.app['logger'].error("Lack of login or password: " + str(e))
            return web.json_response(
                Response(status=ResponseStatus.SERVER_ERROR, reason="Lack of login or password", token='NULL',
                         response_type=ResponseTypes.ERROR))
        except AttributeError as e:
            self.request.app['logger'].error("Authentication failed: " + str(e))
            return web.json_response(
                Response(status=ResponseStatus.SERVER_ERROR, reason='VK Authentication failed.', token='NULL',
                         response_type=ResponseTypes.ERROR))

        if result.is_error():
            self.request.app['logger'].error(result)
            result['token'] = 'NULL'
            return web.json_response(result)

        return web.json_response(Response(status=result['status'], token=vk_api.session.access_token,
                                          response_type=ResponseTypes.AUTH_TOKEN))
