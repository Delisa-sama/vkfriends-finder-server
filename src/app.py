import base64
import hashlib
import os

from aiohttp import web, log
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from src.HTTP.getPosts import HTTPGetPosts
from src.HTTP.login import HTTPLogin
from src.HTTP.logout import HTTPLogout
from src.websocket.getFriends import WSGetFriends
from src.websocket.login import WSLogin
from src.websocket.logout import WSLogout
from src.websocket.root import WSRoot

ROUTES = [
    ('GET', '/ws', 'wsroot', WSRoot),
    ('GET', '/ws/login', 'wslogin', WSLogin),
    ('GET', '/ws/logout', 'wslogout', WSLogout),
    ('GET', '/ws/friends', 'wsgetfriends', WSGetFriends),
    ('POST', '/login', 'httplogin', HTTPLogin),
    ('POST', '/logout', 'httplogout', HTTPLogout),
    ('GET', '/posts', 'httpposts', HTTPGetPosts),
    # TODO: add get_friends and get_posts routes
]


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


middle = [
    session_middleware(
        EncryptedCookieStorage(
            hashlib.sha256(
                base64.urlsafe_b64decode(
                    fernet.Fernet.generate_key()
                )
            ).digest()
        )
    )
]
app = web.Application(middlewares=middle)

for route in ROUTES:
    app.router.add_route(method=route[0], path=route[1], name=route[2], handler=route[3])

if not os.path.exists('./static'):
    os.mkdir('./static')

app['static_root_url'] = '/static'
app.router.add_static('/static', 'static', name='static')

app.on_cleanup.append(on_shutdown)
app['websockets'] = []

log.server_logger.debug('start server')
web.run_app(app)
log.server_logger.debug('Stop server end')
