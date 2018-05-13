from abc import ABCMeta, abstractmethod


class IRestServer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, host: str = '127.0.0.1', port: int = 8888, debug: bool = False) -> None: raise NotImplementedError
