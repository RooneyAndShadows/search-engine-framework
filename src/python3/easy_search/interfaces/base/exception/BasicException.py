
class BasicException(Exception):
    def __init__(self, message: str, prev: Exception = None, code: int = 0) -> None:
        self.message = message
        self.prev = prev
        self.code = code
