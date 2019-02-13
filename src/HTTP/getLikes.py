from aiohttp import web

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
        json = await self.request.json()
        owner_id = 0
        item_id = 874
        print(json)
        result = get_likes(
            api=self.request.app['users'][token].vk_api,
            owner_id=owner_id,
            item_id=item_id,
        )
        return web.json_response(result)
