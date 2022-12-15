from requests.exceptions import HTTPError


class NotLoggedException(HTTPError):

    def __init__(self, error_message: str = '') -> None:
        super().__init__(str(error_message))
        return
