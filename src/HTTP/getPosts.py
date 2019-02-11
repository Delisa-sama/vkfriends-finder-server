from aiohttp import web

from src.Authentication.decorator import authentication


class HTTPGetPosts(web.View):
    @authentication
    async def get(self):
        return web.json_response({
            'status': "OK"
        })
