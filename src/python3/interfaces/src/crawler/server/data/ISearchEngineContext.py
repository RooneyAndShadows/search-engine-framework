from abc import abstractmethod, ABC, ABCMeta

from interfaces.src.crawler.server.data.set.ICrawlerSet import ICrawlerSet
from interfaces.src.crawler.server.data.set.IJobSet import IJobSet


class ISearchEngineContext(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def job_set(self) -> IJobSet: raise NotImplementedError

    @abstractmethod
    def crawler_set(self) -> ICrawlerSet: raise NotImplementedError

    @abstractmethod
    def save(self) -> None: raise NotImplementedError

    @abstractmethod
    def start_transaction(self) -> None: raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None: raise NotImplementedError

    @abstractmethod
    def commit(self) -> None: raise NotImplementedError
