from aiohttp import web

from src.API.user import User
from src.utils import dict_response


class HTTPLogin(web.View):
    """A Class used to represent Web View of Login method via HTTP."""

    async def post(self) -> web.Response:
        """HTTP Authentication Feature.

        :return: JSON response with result information.
        :rtype: web.Reponse
        """
        data = await self.request.post()

        try:
            user = User()
            result = await user.auth(login=data['login'], password=data['password'])
        except KeyError as e:
            self.request.app['logger'].error(str(e))
            return web.json_response(dict_response(status='ERROR', reason=str(e)))
        if result['status'] == 'ERROR':
            return web.json_response(result)

        self.request.app['users'][user.vk_session.access_token] = user
        return web.json_response(result)
