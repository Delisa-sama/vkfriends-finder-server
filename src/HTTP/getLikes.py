from urllib import parse

from aiohttp import web

from src.API.vkapirequest import get_likes
from src.Authentication.decorator import authentication
from src.utils import dict_response


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
        except KeyError as e:
            self.request.app['logger'].error(str(e))
            return web.json_response(dict_response(status='ERROR', reason=str(e)))
        except TypeError as e:
            self.request.app['logger'].error(str(e))
            return web.json_response(dict_response(status='ERROR', reason=str(e)))

        result = await get_likes(
            api=self.request.app['users'][token].vk_api,
            owner_id=owner_id,
            item_id=item_id,
        )

        return web.json_response(result)
