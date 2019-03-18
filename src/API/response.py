from enum import Enum


class ResponseTypes(str, Enum):
    FRIENDS_LIST = 'friends-list'
    USERS_INFO = 'users-info'
    AUTH_TOKEN = 'auth-token'
    LAST_POST = 'last-post'
    UNDEFINED = 'undefined'
    ERROR = 'error'
    LIKES = 'likes'


class ResponseStatus(int, Enum):
    OK = 200
    SERVER_ERROR = 400
    EXTERNAL_ERROR = 500


class Response(dict):
    """A Class used to represent response."""

    def __init__(self, status: ResponseStatus = ResponseStatus.OK,
                 response_type: ResponseTypes = ResponseTypes.UNDEFINED,
                 reason: str = 'OK',
                 **kwargs):
        super().__init__(status=status, type=response_type, reason=reason, **kwargs)

    def is_error(self) -> bool:
        """Method to check is status error

        :return: True if status is 'ERROR' else False
        :rtype: bool
        """
        return self['status'] / 100 != 2

    def is_ok(self) -> bool:
        """Method to check is status OK

        :return: True if status is 'OK' else False
        :rtype: bool
        """
        return self['status'] == 200
