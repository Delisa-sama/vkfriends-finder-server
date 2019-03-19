from datetime import datetime as dt

import vk

from src.API.response import Response, ResponseTypes, ResponseStatus
from src.settings import config


class VkAPI:

    def __init__(self):
        self.api: vk.API = None

    async def get_profileinfo(self):
        try:
            info = self.api.account.getProfileInfo()
            print(info)
            return Response(status=ResponseStatus.OK, info=info, response_type=ResponseTypes.USERS_INFO)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=f'Error in get_profileinfo: {str(e)}',
                            response_type=ResponseTypes.ERROR)

    async def get_info(
            self,
            user_ids: list = None,
            fields: str = 'relation, bdate, photo_200_orig, nickname, online, sex, city, home_town',
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
                for user in info:
                    user_city = user.get('city', {})
                    user['city'] = user_city.get('title', '')
                    user['photoUrl'] = user.get('photo_200_orig', 'https://vk.com/images/camera_200.png?ava=1')
                    del user['photo_200_orig']
                    user['isOnline'] = user.get('online', 0)
                    del user['online']
                    user['firstName'] = user.get('first_name', '')
                    del user['first_name']
                    user['lastName'] = user.get('last_name', '')
                    del user['last_name']
                    del user['is_closed']
                    del user['can_access_closed']


                def _filter(user: dict):
                    def _age(born: str):
                        try:
                            born: dt = dt.strptime(born, '%d.%m.%Y')
                        except ValueError:
                            return 0
                        except TypeError:
                            return 0
                        today = dt.now()
                        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

                    sex: bool = True if filters.get('sex', 0) == 0 \
                        else user.get('sex', 0) == filters.get('sex', 0)

                    relation: bool = True if filters.get('relation', 0) == 0 \
                        else user.get('relation', 0) == filters.get('relation')

                    user_age: int = _age(user.get('bdate'))

                    age: bool = True if user_age == 0 \
                        else filters.get('minAge', 0) <= user_age <= filters.get('maxAge', 100)

                    city: bool = True if filters.get('city') == '' \
                        else user.get('city', '').lower() == filters.get('city').lower() \
                             or user.get('home_town', '').lower() == filters.get('city').lower()

                    return sex and relation and age and city

                info = list(filter(_filter, info))

            return Response(status=ResponseStatus.OK, info=info, response_type=ResponseTypes.USERS_INFO)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=f'Error in get_info: {str(e)}',
                            response_type=ResponseTypes.ERROR)

    async def get_last_post(self,
                            owner_id: int = 0) -> Response:
        try:
            post = self.api.wall.get(owner_id=owner_id, count=1)
            return Response(status=ResponseStatus.OK, post=str(post), response_type=ResponseTypes.LAST_POST)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=f'Error in get_last_post: {str(e)}',
                            response_type=ResponseTypes.ERROR)

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
            print(friends)
            return Response(status=ResponseStatus.OK, friends=friends, response_type=ResponseTypes.FRIENDS_LIST)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=f'Error in get_friends: {str(e)}',
                            response_type=ResponseTypes.ERROR)
        except AttributeError as e:
            return Response(status=ResponseStatus.SERVER_ERROR, reason='Error in get_friends: Not authenticated',
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
            return Response(status=ResponseStatus.OK, likes=user_ids, response_type=ResponseTypes.LIKES)
        except vk.exceptions.VkAPIError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=f'Error in get_likes: {str(e)}',
                            response_type=ResponseTypes.ERROR)

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
                app_id=config['vk_api_app_id'],
                user_login=credentials['login'],
                user_password=credentials['password']
            )

            self.api = vk.API(self.session, v=config.get('vk_api_version'), lang=config.get('vk_api_lang'),
                              timeout=config.getint('vk_api_timeout'))
            return Response(status=ResponseStatus.OK, response_type=ResponseTypes.AUTH_TOKEN)
        except vk.exceptions.VkAuthError as e:
            return Response(status=ResponseStatus.EXTERNAL_ERROR, reason=f'Error in auth: {str(e)}',
                            response_type=ResponseTypes.ERROR)
        except KeyError:
            return Response(status=ResponseStatus.SERVER_ERROR, reason="Lack of login or password",
                            response_type=ResponseTypes.ERROR)
