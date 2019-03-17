import typing
from urllib.parse import parse_qs, urlparse

from aiohttp import web

from src.API.response import Response, ResponseStatus, ResponseTypes


def authentication(func: typing.Callable) -> typing.Callable:
    """A authentication decorator.

    :param func: A function to decorate.
    :rtype: typing.Callable

    :return: Return a wrapper function.
    :rtype: typing.Callable
    """

    async def wrapper(view: web.View) -> web.Response:
        url = urlparse(str(view.request.url))
        query_params = parse_qs(url.query)
        try:
            token = query_params['token'][0]
        except KeyError as e:
            view.request.app['logger'].error("Token not found: " + str(e))
            token = None

        if token in view.request.app['users']:
            view.request.app['logger'].info("User logged in via token.")
            response = await func(view, token)
        elif url.scheme == 'ws':
            view.request.app['logger'].info("User authentication error when connect via WebSocket.")
            response = web.WebSocketResponse()
            await response.prepare(view.request)
            await response.send_json(
                Response(status=ResponseStatus.SERVER_ERROR, reason="Not valid token, login please.",
                         response_type=ResponseTypes.ERROR))
        else:
            view.request.app['logger'].info("User authentication error when connect via HTTP.")
            response = web.json_response(
                Response(status=ResponseStatus.SERVER_ERROR, reason="Not authenticated token, login please.",
                         response_type=ResponseTypes.ERROR))

        return response

    return wrapper
