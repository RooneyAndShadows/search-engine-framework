from abc import ABCMeta, abstractmethod
from uuid import UUID

from ..data.JobData import JobData
from ..entity.Job import Job


class IJobSet:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, job: JobData) -> UUID: raise NotImplementedError

    @abstractmethod
    def edit(self, job_id: UUID, job: JobData) -> None: raise NotImplementedError

    @abstractmethod
    def delete(self, job_id: UUID) -> None: raise NotImplementedError

    @abstractmethod
    def get(self, job_id: UUID) -> Job: raise NotImplementedError

    @abstractmethod
    def get_by_hash(self, unique_hash: str) -> Job: raise NotImplementedError

    @abstractmethod
    def get_next_free(self) -> Job: raise NotImplementedError

    @abstractmethod
    def lock(self, job_id: UUID) -> None: raise NotImplementedError

    @abstractmethod
    def unlock(self, job_id: UUID) -> None: raise NotImplementedError
