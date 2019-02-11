from src.API.vkapirequest import VKAPIRequest


class User:

    def __init__(self, data):
        self.login = data['login']
        self.password = data['password']
        self.vk_api = None
        self.vk_session = None

    async def vk_auth(self):
        req = VKAPIRequest()
        result = await req.auth({'login': self.login, 'password': self.password})
        if result['status'] == 'ERROR':
            return result
        else:
            self.vk_api = result['vk_api']
            self.vk_session = result['vk_session']
            return result


pool = dict()
