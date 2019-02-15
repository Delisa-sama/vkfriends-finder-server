def dict_response(status: str = 'OK',
                  **kwargs) -> dict:
    """Рelper function for easy dictionary response creation

    :param status: Status of the operation
    :type: str

    :param kwargs: Keyworded parameters
    :return: Dictionary type response

    :rtype: dict
    """
    d = {'status': status}
    for key, value in kwargs.items():
        d[key] = value

    return d
