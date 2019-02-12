from http import HTTPStatus
from urllib.parse import parse_qs, urlparse

from aiohttp import web


def authentication(func):
    async def wrapper(view: web.View):
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
            await response.send_json({'status': HTTPStatus.UNAUTHORIZED,
                                      'reason': "Not authenticated token, login please."})
        else:
            response = web.json_response({'status': HTTPStatus.UNAUTHORIZED,
                                          'reason': "Not authenticated token, login please."})

        return response

    return wrapper
