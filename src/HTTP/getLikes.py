from urllib import parse

from aiohttp import web

from src.API.response import Response
from src.API.vkapirequest import get_likes
from src.Authentication.decorator import authentication


class HTTPGetLikes(web.View):
    """A Class used to represent Web View of GetLikes method via HTTP."""

    @authentication
    async def get(self, token: str) -> web.Response:
        """The function allows you to take information about the users who liked the given post.

        :param token: Token of current user.
        :type: str

        :return: JSON response with result information.
        :rtype: web.Response
        """
        try:
            owner_id, item_id = parse.urlparse(self.request.query['url']).query[6:].split('_')
        except KeyError:
            self.request.app['logger'].error("URL parse error.")
            return web.json_response(Response(status='ERROR', reason="URL parse error."))

        result = await get_likes(
            api=self.request.app['users'][token].vk_api,
            owner_id=owner_id,
            item_id=item_id,
        )
        self.request.app['logger'].info("HTTPGetLikes.get called.")

        return web.json_response(result)
