from http import HTTPStatus


class Response:
    def __init__(self, status=HTTPStatus.OK, exception=None, objects=None):
        if objects is None:
            objects = dict()
        self.objects = objects

        self.status = status
        self.exception = exception if exception else ''

    def __dict__(self):
        return {
            'status': self.status,
            'exception': self.exception
        }
