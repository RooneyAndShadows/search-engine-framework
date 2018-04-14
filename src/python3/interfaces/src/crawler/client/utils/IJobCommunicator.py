from abc import ABC, abstractmethod

from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.communication.response.JobInformation import JobInformation


class IJobCommunicator(object):
    __metaclass__ = ABC

    @abstractmethod
    def get_next_job(self) -> JobInformation: raise NotImplementedError

    @abstractmethod
    def finish_job(self, result: JobResult) -> None: raise NotImplementedError
