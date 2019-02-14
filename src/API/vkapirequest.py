import vk

from src.settings import VK_API_APP_ID, VK_API_TIMEOUT, VK_API_LANG, VK_API_VERSION
from src.utils import dict_response


async def get_info(
        api: vk.api,
        user_ids: list = None):
    """The function allows you to take extended information about users.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param user_ids: List of user ids about which you need to get extended information.
    :type: list
    """
    pass


async def get_friends(
        api: vk.api,
        target_id: int = 0) -> dict:
    """The function allows you to take information about friends of target user.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param target_id: Id of target user.
    :type: int

    :return: A dictionary with the status of the operation and the result of its execution.
    :rtype: dict
    """
    try:
        friends = api.friends.get(user_id=target_id)
    except vk.exceptions.VkAPIError as e:
        return dict_response(status='ERROR', reason=str(e))
    except AttributeError as e:
        return dict_response(status='ERROR', reason='Not authenticated')

    return dict_response(status='OK', friends=str(friends))


async def get_likes(
        api: vk.api,
        item_id: int,
        owner_id: int = 0) -> dict:
    """A function that returns information about people who liked the post with the specified id.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param item_id: Post id relative to owner_id.
    :type: int

    :param owner_id: Id of wall owner.
    :type: int

    :return: Dictionary with operation status and user list.
    :rtype: dict
    """
    try:
        likes_people = api.likes.getList(
            type='post',
            owner_id=owner_id,
            item_id=item_id,
            extended=1,
        )
    except vk.exceptions.VkAPIError as e:
        return dict_response(status='ERROR', reason=str(e))

    return dict_response(status='OK', likes=likes_people)


async def auth(credentials: dict) -> dict:
    """User authentication function through VK API.

    Initializes vk_session and vk_api.

    :param credentials: Dictionary with E-Mail or phone by login key, and password by password key.
    :type: dict

    :return: Dictionary with status operations and initialized objects vk_api and vk_session.
    :rtype: dict
    """
    try:
        vk_session = vk.AuthSession(
            app_id=VK_API_APP_ID,
            user_login=credentials['login'],
            user_password=credentials['password']
        )
        vk_api = vk.API(vk_session, v=VK_API_VERSION, lang=VK_API_LANG, timeout=VK_API_TIMEOUT)
    except vk.exceptions.VkAuthError as e:
        return dict_response(status='ERROR', reason=str(e))
    return dict_response(status='OK', vk_api=vk_api, vk_session=vk_session)
