from abc import ABCMeta
from typing import List
from uuid import UUID

from ..common.JobDescription import JobDescription


class JobResult(object):
    __metaclass__ = ABCMeta

    def __init__(self, job_id: UUID, job_list: List[JobDescription]):
        self.job_id = job_id
        self.job_list = job_list
