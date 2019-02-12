from src.API.vkapirequest import auth as vk_auth


class User:

    def __init__(self,
                 login: str,
                 password: str):
        self.login = login
        self.password = password
        self.vk_api = None
        self.vk_session = None

    async def auth(self):
        result = await vk_auth({'login': self.login, 'password': self.password})
        if result['status'] == 'ERROR':
            return result
        else:
            self.vk_api = result['vk_api']
            self.vk_session = result['vk_session']
            return result
