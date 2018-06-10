from uuid import UUID

from easy_search.interfaces.base.job.JobDescription import JobDescription
from easy_search.interfaces.base.enum import JobType


class ExtendedJobDescription(JobDescription):
    def __init__(self, job_id: UUID, job_type: JobType, target: str, plugin: str):
        super().__init__(job_type, target, plugin)
        self.job_id = job_id
