from aiohttp import web

from src.Authentication.decorator import authentication


class HTTPLogout(web.View):
    @authentication
    async def get(self):
        return web.json_response({
            'status': "OK"
        })
