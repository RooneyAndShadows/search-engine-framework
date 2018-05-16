from abc import ABCMeta, abstractmethod
from typing import List
from uuid import UUID

from ...communication.request.JobResult import JobResult
from ...communication.response.BaseResponse import BaseResponse
from ...communication.response.JobInformation import JobInformation


class IJobScheduler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_next_job(self, crawler_id: UUID, available_plugins: List[str]) -> JobInformation: raise NotImplementedError

    @abstractmethod
    def finish_job(self, crawler_id: UUID, result: JobResult) -> BaseResponse: raise NotImplementedError
