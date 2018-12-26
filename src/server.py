import base64

import aiohttp_session
import vk
from aiohttp import web
from aiohttp_session import get_session
from aiohttp_session.nacl_storage import NaClCookieStorage
from cryptography import fernet

vk_session = None
vk_api = None


async def session_handler(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    if last_visit is None:
        return web.json_response({'session': 'Last visit is None'})
    else:
        return web.json_response({'session': str(last_visit)})


async def auth(request):
    login = request.query['login']
    password = request.query['password']

    # return web.Response(text='{}: {}'.format(login, password))
    session = await aiohttp_session.new_session(request)
    try:
        vk_session = vk.AuthSession(app_id='6798117', user_login=login, user_password=password)
        session['vk_api'] = vk.API(vk_session, v='5.35', lang='ru', timeout=10)
    except vk.exceptions.VkAuthError as e:
        return web.json_response({'error': str(e)})

    return web.Response(text='Auth successful: {}'.format(login))


async def get_friends(request):
    session = await aiohttp_session.get_session(request)
    user_id = request.query['id']
    friends = None
    try:
        friends = session['vk_api'].friends.get(user_id=user_id)
    except vk.exceptions.VkAPIError as e:
        return web.json_response({'error': str(e)})
    #    except AttributeError as e:
    #       return web.json_response({'error': 'Not authenticated'})

    return web.Response(text=str(friends))


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})


async def root(request):
    return web.Response(text=str(vk_session))


fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
storage = aiohttp_session.nacl_storage.NaClCookieStorage(secret_key)
app = web.Application()
aiohttp_session.setup(app, storage)
app.add_routes([
    web.get('/get_friends', get_friends),
    web.get('/auth', auth),
    web.get('/', root)
])

web.run_app(app)
