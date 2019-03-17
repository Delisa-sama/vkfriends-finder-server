import datetime

import vk

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.settings import VK_API_APP_ID, VK_API_TIMEOUT, VK_API_LANG, VK_API_VERSION


class VkAPI:

    def __init__(self):
        self.api: vk.API = None

    async def get_profileinfo(self):
        try:
            info = self.api.account.getProfileInfo()
            return Response(status=ResponseStatus.OK, info=info, response_type=ResponseTypes.USERS_INFO)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)

    async def get_info(
            self,
            user_ids: list = None,
            fields: str = 'relation, bdate, photo_200_orig, nickname, online, sex, city',
            filters: dict = None) -> Response:
        """The function allows you to take extended information about users.

        :param api: A VKAPI of current user.
        :type: vk.api

        :param user_ids: List of user ids about which you need to get extended information.
        :type: list

        :param fields: Set of fields (VK Api) to return in response. Example: "field1, field2".
        :type: str
        """
        try:
            print(user_ids)
            info = self.api.users.get(user_ids=user_ids, fields=fields)
            print(info)
            if filters is not None:
                def calculate_age(born):
                    today = datetime.datetime.now()
                    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

                info = list(filter(lambda x: x['sex'] == filters['sex']
                                             and x.get('relation', 0) == filters['relation']
                                             and filters['minAge']
                                             < calculate_age(datetime.datetime.strptime(x['bdate'], "%d.%m.%Y"))
                                             < filters['maxAge']
                                             and (x['city'].get('title', "") == filters['city']
                                                  and filters['city'] != ""),
                                   info))

            return Response(status=ResponseStatus.OK, info=info, response_type=ResponseTypes.USERS_INFO)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)

    async def get_last_post(self,
                            owner_id: int = 0) -> Response:
        try:
            post = self.api.wall.get(owner_id=owner_id, count=1)
            return Response(status=ResponseStatus.OK, post=str(post), response_type=ResponseTypes.LAST_POST)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)

    async def get_friends(
            self,
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
            friends = self.api.friends.get(user_id=target_id, fields=fields)
            return Response(status=ResponseStatus.OK, friends=friends, response_type=ResponseTypes.FRIENDS_LIST)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)
        except AttributeError as e:
            return Response(status=ResponseStatus.SERVER_ERROR, reason='Not authenticated',
                            response_type=ResponseTypes.ERROR)

    async def get_likes(
            self,
            item_id: int,
            owner_id: int = 0) -> Response:
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
            likes_people = self.api.likes.getList(
                type='post',
                owner_id=owner_id,
                item_id=item_id,
            )
            user_ids = [id for id in likes_people['items']]
            return Response(status=ResponseStatus.OK, likes=user_ids, reason='OK', response_type=ResponseTypes.LIKES)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)

    async def auth(self, credentials: dict) -> Response:
        """User authentication function through VK API.

        Initializes vk_session and vk_api.

        :param credentials: Dictionary with E-Mail or phone by login key, and password by password key.
        :type: dict

        :return: Dictionary with status operations and initialized objects vk_api and vk_session.
        :rtype: Response
        """
        try:
            self.session = vk.AuthSession(
                app_id=VK_API_APP_ID,
                user_login=credentials['login'],
                user_password=credentials['password']
            )

            self.api = vk.API(self.session, v=VK_API_VERSION, lang=VK_API_LANG, timeout=VK_API_TIMEOUT)
            return Response(status=ResponseStatus.OK, response_type=ResponseTypes.AUTH_TOKEN)
        except vk.exceptions.VkAuthError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=str(e), response_type=ResponseTypes.ERROR)
        except KeyError:
            return Response(status=ResponseStatus.SERVER_ERROR, reason="Lack of login or password",
                            response_type=ResponseTypes.ERROR)
