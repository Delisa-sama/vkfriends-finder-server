from aiohttp import web

from src.API.user import User


class HTTPLogin(web.View):
    async def post(self):
        data = await self.request.post()
        user = User(data)

        result = await user.vk_auth()
        if result['status'] == 'ERROR':
            return web.json_response(result)

        # TODO add user to session
