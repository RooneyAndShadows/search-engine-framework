from uuid import UUID

from easy_search.interfaces.crawler.communication.common.JobDescription import JobDescription
from ...enum.JobType import JobType


class ExtendedJobDescription(JobDescription):
    def __init__(self, job_id: UUID, job_type: JobType, target: str, plugin: str):
        super().__init__(job_type, target, plugin)
        self.job_id = job_id
