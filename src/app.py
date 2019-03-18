import base64
import hashlib
import os

from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from src.HTTP.getLikes import HTTPGetLikes
from src.HTTP.login import HTTPLogin
from src.HTTP.logout import HTTPLogout
from src.WS.getFriends import WSGetFriends
from src.WS.login import WSLogin
from src.WS.logout import WSLogout
from src.logger import init_logger
from src.settings import config

ROUTES = [
    ('GET', '/ws/login', 'wslogin', WSLogin),
    ('GET', '/ws/logout', 'wslogout', WSLogout),
    ('GET', '/ws/friends', 'wsgetfriends', WSGetFriends),
    ('POST', '/login', 'httplogin', HTTPLogin),
    ('POST', '/logout', 'httplogout', HTTPLogout),
    ('POST', '/likes', 'httpposts', HTTPGetLikes),
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

app = web.Application()

for route in ROUTES:
    app.router.add_route(method=route[0], path=route[1], name=route[2], handler=route[3])

static_path = config.get("static_path")
if not os.path.exists(static_path):
    os.mkdir(static_path)

app['static_root_url'] = config.get('static_path')
app.router.add_static(prefix='/static', path='static', name='static')
app.router.add_static(prefix='/', path='static', name='index')

app.on_cleanup.append(on_shutdown)

app['websockets'] = []
app['logger'] = init_logger()
app['users'] = dict()

app['logger'].info("Start")
try:
    web.run_app(app, port=config.getint('port'))
except OSError as e:
    app['logger'].error(f"Port: {config.getint('port')} is already in use.")
app['logger'].info("Server closing")
