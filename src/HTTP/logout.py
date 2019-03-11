from aiohttp import web

from src.Decorators.authentication import authentication


class HTTPLogout(web.View):
    """A Class used to represent Web View of Logout method via HTTP."""

    @authentication
    async def get(self, token: str) -> web.Response:
        return web.json_response({
            'status': "OK"
        })
