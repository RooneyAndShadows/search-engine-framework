from abc import ABCMeta, abstractmethod
from uuid import UUID

from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.communication.response.BaseResponse import BaseResponse
from interfaces.src.crawler.communication.response.JobInformation import JobInformation


class IJobScheduler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_next_job(self, crawler_id: UUID) -> JobInformation: raise NotImplementedError

    @abstractmethod
    def finish_job(self, crawler_id: UUID, result: JobResult) -> BaseResponse: raise NotImplementedError
