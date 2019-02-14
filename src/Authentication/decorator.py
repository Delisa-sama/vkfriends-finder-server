import typing
from urllib.parse import parse_qs, urlparse

from aiohttp import web

from src.utils import dict_response


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
            view.request.app['logger'].error(str(e))
            token = None

        if token in view.request.app['users']:
            response = await func(view, token)
        elif url.scheme == 'ws':
            response = web.WebSocketResponse()
            await response.prepare(view.request)
            await response.send_json(dict_response(status='ERROR', reason="Not authenticated token, login please."))
        else:
            response = web.json_response(
                dict_response(status='ERROR', reason="Not authenticated token, login please."))

        return response

    return wrapper
