class Response(dict):
    """A Class used to represent response."""

    def __init__(self, status: str = 'OK', **kwargs):
        super().__init__(status=status, **kwargs)

    def is_error(self) -> bool:
        """Method to check is status error

        :return: True if status is 'ERROR' else False
        :rtype: bool
        """
        return self['status'] == 'ERROR'

    def is_ok(self) -> bool:
        """Method to check is status OK

        :return: True if status is 'OK' else False
        :rtype: bool
        """
        return self['status'] == 'OK'
