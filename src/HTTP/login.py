from aiohttp import web

from src.API.user import User


class HTTPLogin(web.View):
    async def post(self):
        data = await self.request.post()

        user = User(login=data['login'], password=data['password'])

        result = await user.vk_auth()
        if result['status'] == 'ERROR':
            return web.json_response(result)

        self.request.app['users'][user.vk_session.access_token] = user
        return web.json_response(result)
