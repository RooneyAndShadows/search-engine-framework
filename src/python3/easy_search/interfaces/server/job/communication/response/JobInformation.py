from easy_search.interfaces.base.job.ExtendedJobDescription import ExtendedJobDescription
from easy_search.interfaces.base.communication.response.BaseResponse import BaseResponse


class JobInformation(BaseResponse):
    def __init__(self, job_desc: ExtendedJobDescription = None):
        result = job_desc is not None
        super().__init__(result)
        self.job_desc = job_desc
