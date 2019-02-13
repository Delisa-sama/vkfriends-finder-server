from aiohttp import web

from src.API.user import User


class HTTPLogin(web.View):
    """A Class used to represent Web View of Login method via HTTP."""

    async def post(self) -> web.Response:
        """HTTP Authentication Feature.

        :return: JSON response with result information.
        :rtype: web.Reponse
        """
        data = await self.request.post()

        user = User()
        result = await user.auth(login=data['login'], password=data['password'])
        if result['status'] == 'ERROR':
            return web.json_response(result)

        self.request.app['users'][user.vk_session.access_token] = user
        return web.json_response(result)
