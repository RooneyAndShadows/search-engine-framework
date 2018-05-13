from abc import ABC, abstractmethod

from ...communication.request.JobResult import JobResult
from ...communication.response.JobInformation import JobInformation


class IJobCommunicator(object):
    __metaclass__ = ABC

    @abstractmethod
    def get_next_job(self) -> JobInformation: raise NotImplementedError

    @abstractmethod
    def finish_job(self, result: JobResult) -> None: raise NotImplementedError
