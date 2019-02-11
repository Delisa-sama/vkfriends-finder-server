import vk

from src.settings import VK_API_APP_ID, VK_API_TIMEOUT, VK_API_LANG, VK_API_VERSION


class VKAPIRequest:

    async def get_friends(self, user, id):
        friends = None
        try:
            friends = user.vk_api.friends.get(user_id=id)
        except vk.exceptions.VkAPIError as e:
            return {'status': 'ERROR', 'exception': str(e)}
        except AttributeError as e:
            return {'status': 'ERROR', 'exception': 'Not authenticated'}

        return {'status': 'OK', "friends": str(friends)}

    async def get_posts(self):
        # TODO: get posts from VKAPI
        return {"posts": [12234, 2325421, 4535345]}

    async def auth(self, user):
        try:
            vk_session = vk.AuthSession(app_id=VK_API_APP_ID, user_login=user['login'], user_password=user['password'])
            vk_api = vk.API(vk_session, v=VK_API_VERSION, lang=VK_API_LANG, timeout=VK_API_TIMEOUT)
        except vk.exceptions.VkAuthError as e:
            return {'status': 'ERROR', 'exception': str(e)}
        return {'status': 'OK', 'vk_api': vk_api, 'vk_session': vk_session}
