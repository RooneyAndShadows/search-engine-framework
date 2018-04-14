from abc import ABCMeta
from uuid import UUID


class JobResult(object):
    __metaclass__ = ABCMeta

    def __init__(self, job_id: UUID, job_list: list):
        self.job_id = job_id
        self.job_list = job_list
