from aiohttp import web

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.Decorators.authentication import authentication
from src.HTTP.Response import json_response


class HTTPGetLikedPeoples(web.View):
    """A Class used to represent Web View of GetLikedPeoples method via HTTP."""

    @authentication
    async def post(self, token: str) -> web.Response:
        """The function allows you to take information about the users who liked the given post.

        :param token: Token of current user.
        :type: str

        :return: JSON response with result information.
        :rtype: web.Response
        """
        try:
            request = await self.request.json()
            owner_id, item_id = request['url'].split('wall')[1].split('_')  # /wall{owner_id}_{item_id}
            filters = request['filterKit']
            print(f'Filters: {filters}')
        except Exception:
            self.request.app['logger'].error("URL parse error.")
            return web.json_response(Response(status=ResponseStatus.SERVER_ERROR, reason="URL parse error.",
                                              response_type=ResponseTypes.ERROR))
        api = self.request.app['users'][token]
        user_ids = await api.get_liked_people(
            owner_id=owner_id,
            item_id=item_id,
        )
        print(f"Liked users: {user_ids.get('likes')}")
        result = await api.get_info(user_ids=user_ids.get('likes'), filters=filters)
        self.request.app['logger'].info("HTTPGetLikedPeoples.get called.")

        return json_response(result)
