from interfaces.src.crawler.communication.response.BaseResponse import BaseResponse
from interfaces.src.crawler.enum.JobType import JobType


class JobInformation(BaseResponse):
    def __init__(self, job_type: JobType = None, target: str = None):
        result = job_type is not None and target is not None
        super().__init__(result)
        self.job_type = job_type
        self.target = target
