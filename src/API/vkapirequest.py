import vk

from src.API.response import Response
from src.settings import VK_API_APP_ID, VK_API_TIMEOUT, VK_API_LANG, VK_API_VERSION


async def get_info(
        api: vk.api,
        user_ids: list = None,
        filters: dict = None) -> Response:
    """The function allows you to take extended information about users.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param user_ids: List of user ids about which you need to get extended information.
    :type: list
    """
    try:
        # TODO: Add filters
        info = api.users.get(user_ids=user_ids)
        return Response(status='OK', info=str(info))
    except vk.exceptions.VkAPIError as e:
        return Response(status='ERROR', reason=str(e))


async def get_friends(
        api: vk.api,
        target_id: int = 0) -> Response:
    """The function allows you to take information about friends of target user.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param target_id: Id of target user.
    :type: int

    :return: A dictionary with the status of the operation and the result of its execution.
    :rtype: Response
    """
    try:
        friends = api.friends.get(user_id=target_id)
        return Response(status='OK', friends=str(friends))
    except vk.exceptions.VkAPIError as e:
        return Response(status='ERROR', reason=str(e))
    except AttributeError as e:
        return Response(status='ERROR', reason='Not authenticated')


async def get_likes(
        api: vk.api,
        item_id: int,
        owner_id: int = 0,
        filters: dict = None) -> Response:
    """A function that returns information about people who liked the post with the specified id.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param item_id: Post id relative to owner_id.
    :type: int

    :param owner_id: Id of wall owner.
    :type: int

    :return: Dictionary with operation status and user list.
    :rtype: Response
    """
    try:
        likes_people = api.likes.getList(
            type='post',
            owner_id=owner_id,
            item_id=item_id,
            extended=1,
        )
        user_ids = [user['id'] for user in likes_people['items']]
        users_info = await get_info(api=api,
                                    user_ids=user_ids,
                                    filters=filters)
        return Response(status='OK', likes=users_info)
    except vk.exceptions.VkAPIError as e:
        return Response(status='ERROR', reason=str(e))


async def auth(credentials: dict) -> Response:
    """User authentication function through VK API.

    Initializes vk_session and vk_api.

    :param credentials: Dictionary with E-Mail or phone by login key, and password by password key.
    :type: dict

    :return: Dictionary with status operations and initialized objects vk_api and vk_session.
    :rtype: Response
    """
    try:
        vk_session = vk.AuthSession(
            app_id=VK_API_APP_ID,
            user_login=credentials['login'],
            user_password=credentials['password']
        )
        vk_api = vk.API(vk_session, v=VK_API_VERSION, lang=VK_API_LANG, timeout=VK_API_TIMEOUT)
        return Response(status='OK', vk_api=vk_api, vk_session=vk_session)
    except vk.exceptions.VkAuthError as e:
        return Response(status='ERROR', reason=str(e))
    except KeyError:
        return Response(status='ERROR', reason="Lack of login or password")
