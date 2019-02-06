from aiohttp import web
from aiohttp_session import get_session

from src.auth.user import User


class Login(web.View):

    async def get(self):
        session = await get_session(self.request)
        # TODO: check user in session

    async def post(self):
        data = await self.request.post()
        user = User(data)

        result = await user.vk_auth()
        if result['status'] == 'ERROR':
            return web.json_response(result)

        session = await get_session(self.request)
        # TODO add user to session
