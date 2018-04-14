from interfaces.src.crawler.communication.response.Error import Error


class BaseResponse(object):
    def __init__(self, is_successful: bool = False):
        self.is_successful = is_successful
        self.error = None

    def set_error(self, error: Error) -> None:
        self.error = error

    def has_error(self) -> bool:
        return self.error is not None
