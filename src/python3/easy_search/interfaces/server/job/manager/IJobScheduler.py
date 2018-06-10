from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from easy_search.interfaces.server.job.communication.request.JobResult import JobResult
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse
from easy_search.interfaces.server.job.communication.response.JobInformation import JobInformation


class IJobScheduler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_next_job(self, crawler_id: UUID, available_plugins: List[str]) -> JobInformation: raise NotImplementedError

    @abstractmethod
    def finish_job(self, crawler_id: UUID, result: JobResult) -> BaseResponse: raise NotImplementedError
