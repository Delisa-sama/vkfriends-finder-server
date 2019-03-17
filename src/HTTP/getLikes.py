from urllib import parse

from aiohttp import web

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.Decorators.authentication import authentication


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
            fields = await self.request.json()
            owner_id, item_id = parse.urlparse(fields['url']).query[6:].split('_')
        except KeyError:
            self.request.app['logger'].error("URL parse error.")
            return web.json_response(Response(status=ResponseStatus.SERVER_ERROR, reason="URL parse error.",
                                              response_type=ResponseTypes.ERROR))
        api = self.request.app['users'][token]
        result = await api.get_likes(
            owner_id=owner_id,
            item_id=item_id,
            fields=fields,
        )
        self.request.app['logger'].info("HTTPGetLikes.get called.")

        return web.json_response(result)
