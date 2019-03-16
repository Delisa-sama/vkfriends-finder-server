import vk

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.settings import VK_API_APP_ID, VK_API_TIMEOUT, VK_API_LANG, VK_API_VERSION


async def get_profileinfo(api: vk.api):
    try:
        info = api.account.getProfileInfo()
        return Response(status=ResponseStatus.OK, info=str(info), response_type=ResponseTypes.USERS_INFO)
    except vk.exceptions.VkAPIError as e:
        return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)


async def get_info(
        api: vk.api,
        user_ids: list = None,
        fields: str = '') -> Response:
    """The function allows you to take extended information about users.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param user_ids: List of user ids about which you need to get extended information.
    :type: list

    :param fields: Set of fields (VK Api) to return in response. Example: "field1, field2".
    :type: str
    """
    try:
        info = api.users.get(user_ids=user_ids, fields=fields)
        return Response(status=ResponseStatus.OK, info=str(info), response_type=ResponseTypes.USERS_INFO)
    except vk.exceptions.VkAPIError as e:
        return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)


async def get_last_post(api: vk.api,
                        owner_id: int = 0) -> Response:
    try:
        post = api.wall.get(owner_id=owner_id, count=1)
        return Response(status=ResponseStatus.OK, post=str(post), response_type=ResponseTypes.LAST_POST)
    except vk.exceptions.VkAPIError as e:
        return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)


async def get_friends(
        api: vk.api,
        target_id: int = 0,
        fields: str = '') -> Response:
    """The function allows you to take information about friends of target user.

    :param api: A VKAPI of current user.
    :type: vk.api

    :param target_id: Id of target user.
    :type: int

    :param fields: Set of fields (VK Api) to return in response. Example: "field1, field2".
    :type: str

    :return: A dictionary with the status of the operation and the result of its execution.
    :rtype: Response
    """
    try:
        friends = api.friends.get(user_id=target_id, fields=fields)
        return Response(status=ResponseStatus.OK, friends=str(friends), response_type=ResponseTypes.FRIENDS_LIST)
    except vk.exceptions.VkAPIError as e:
        return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)
    except AttributeError as e:
        return Response(status=ResponseStatus.SERVER_ERROR, reason='Not authenticated',
                        response_type=ResponseTypes.ERROR)


async def get_likes(
        api: vk.api,
        item_id: int,
        owner_id: int = 0,
        fields: str = '') -> Response:
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
                                    fields=fields)
        return Response(status=ResponseStatus.OK, likes=users_info, reason='OK', response_type=ResponseTypes.LIKES)
    except vk.exceptions.VkAPIError as e:
        return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)


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
        return Response(status=ResponseStatus.OK, vk_api=vk_api, vk_session=vk_session,
                        response_type=ResponseTypes.AUTH_TOKEN)
    except vk.exceptions.VkAuthError as e:
        return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)
    except KeyError:
        return Response(status=ResponseStatus.SERVER_ERROR, reason="Lack of login or password",
                        response_type=ResponseTypes.ERROR)
