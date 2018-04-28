from abc import ABCMeta, abstractmethod


class IRestServer:
    __metaclass__ = ABCMeta
    JOB_REGISTER_PATH = "/job/register"
    JOB_FETCH_PATH = "/job/next"

    FORBIDDEN = 403
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SUCCESS = 200

    @abstractmethod
    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None: raise NotImplementedError
