from interfaces.src.base.exception.BasicException import BasicException


class DataAccessException(BasicException):
    def __init__(self, message: str, prev: Exception = None, code: int = 0) -> None:
        super().__init__(message, prev, code)
