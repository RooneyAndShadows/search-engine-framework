from abc import abstractmethod, ABC
from uuid import UUID

from ..entity.Crawler import Crawler


class ICrawlerSet(ABC):

    @abstractmethod
    def register_call(self, crawler_id: UUID) -> None: raise NotImplementedError

    @abstractmethod
    def exists(self, crawler_id: UUID) -> bool: raise NotImplementedError

    @abstractmethod
    def get(self, crawler_id: UUID) -> Crawler: raise NotImplementedError
