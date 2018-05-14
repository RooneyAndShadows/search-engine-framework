from abc import ABC, abstractmethod

from ...communication.common.JobDescription import JobDescription
from ...communication.request.JobResult import JobResult


class IJobCommunicator:
    __metaclass__ = ABC

    @abstractmethod
    def get_next_job(self) -> JobDescription: raise NotImplementedError

    @abstractmethod
    def finish_job(self, result: JobResult) -> None: raise NotImplementedError
