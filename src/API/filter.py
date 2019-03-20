from datetime import datetime as dt


def user_filter(users: dict,
                filters: dict):
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
        if user_age == 0:
            user['bdate'] = ''
        age: bool = True if user_age == 0 \
            else filters.get('minAge', 0) <= user_age <= filters.get('maxAge', 100)
        city: bool = True if filters.get('city') == '' \
            else user.get('city').lower() == filters.get('city').lower()

        return sex and relation and age and city

    if filters is not None:
        for user in users:
            try:
                user_city = user.get('city', {})
                user['city'] = user_city.get('title', user.get('home_town', ''))
                user['photoUrl'] = user.get('photo_200_orig', 'https://vk.com/images/camera_200.png?ava=1')
                del user['photo_200_orig']
                user['isOnline'] = user.get('online', 0)
                del user['online']
                user['firstName'] = user.get('first_name', '')
                del user['first_name']
                user['lastName'] = user.get('last_name', '')
                del user['home_town']
                del user['last_name']
                del user['is_closed']
                del user['can_access_closed']
            except KeyError:
                pass

    return list(filter(_filter, users))
