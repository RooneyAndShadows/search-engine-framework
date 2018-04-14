
class Error(object):
    def __init__(self, err_type: str, code: int, message: str) -> None:
        self.error_type = err_type
        self.code = code
        self.message = message


