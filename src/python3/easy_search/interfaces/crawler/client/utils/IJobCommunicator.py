from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from ...communication.common.ExtendedJobDescription import ExtendedJobDescription
from ...communication.request.JobResult import JobResult


class IJobCommunicator:
    __metaclass__ = ABC

    @abstractmethod
    def get_next_job(self, available_plugins: List[str]) -> ExtendedJobDescription: raise NotImplementedError

    @abstractmethod
    def finish_job(self, result: JobResult) -> None: raise NotImplementedError

    @abstractmethod
    def delete_job(self, job_id: UUID) -> None: raise NotImplementedError
