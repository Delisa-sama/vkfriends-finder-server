from src.API.response import Response
from src.API.vkapirequest import auth as vk_auth


class User:
    """A Class used to represent current user."""

    def __init__(self):
        """Inits User class."""
        self.vk_api = None
        self.vk_session = None

    async def auth(self,
                   password: str,
                   login: str) -> Response:
        """User authentication through VK.

        :param password: User VK password
        :type: str

        :param login: E-Mail or user phone from VK
        :type: str

        :return: Dictionary with authentication result
        :rtype: dict
        """
        result = await vk_auth({'login': login, 'password': password})
        if result.is_ok():
            self.vk_api = result['vk_api']
            self.vk_session = result['vk_session']
        return result
