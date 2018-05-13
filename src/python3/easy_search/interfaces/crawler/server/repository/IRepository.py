from abc import ABCMeta, abstractmethod
from uuid import UUID


class IRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def finish_job(self, job_id: UUID, crawler_id: UUID) -> None: raise NotImplementedError
