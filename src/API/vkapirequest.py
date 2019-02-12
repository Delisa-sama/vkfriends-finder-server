import vk

from src.settings import VK_API_APP_ID, VK_API_TIMEOUT, VK_API_LANG, VK_API_VERSION


async def get_friends(
        api: vk.api,
        target_id: int):
    friends = None
    try:
        friends = api.friends.get(user_id=target_id)
    except vk.exceptions.VkAPIError as e:
        return {'status': 'ERROR', 'reason': str(e)}
    except AttributeError as e:
        return {'status': 'ERROR', 'reason': 'Not authenticated'}

    return {'status': 'OK', "friends": str(friends)}


async def get_posts(*args):
    # TODO: get posts from VKAPI
    return {"posts": [12234, 2325421, 4535345]}


async def auth(credentials: dict):
    try:
        vk_session = vk.AuthSession(
            app_id=VK_API_APP_ID,
            user_login=credentials['login'],
            user_password=credentials['password']
        )
        vk_api = vk.API(vk_session, v=VK_API_VERSION, lang=VK_API_LANG, timeout=VK_API_TIMEOUT)
    except vk.exceptions.VkAuthError as e:
        return {'status': 'ERROR', 'reason': str(e)}
    return {'status': 'OK', 'vk_api': vk_api, 'vk_session': vk_session}
