from urllib import parse

from aiohttp import web

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.Decorators.authentication import authentication


class HTTPGetUsersInfo(web.View):
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
            ids = parse.urlparse(self.request.query['ids'])
        except KeyError:
            self.request.app['logger'].error("URL parse error.")
            return web.json_response(Response(status=ResponseStatus.SERVER_ERROR, reason="URL parse error.",
                                              response_type=ResponseTypes.ERROR))
        api = self.request.app['users'][token]
        result = await api.get_info(
            user_ids=ids
        )
        self.request.app['logger'].info("HTTPGetLikedPeoples.get called.")

        return web.json_response(result)
