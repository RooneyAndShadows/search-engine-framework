from abc import ABC, abstractmethod

from ...communication.common.JobDescription import JobDescription
from ...communication.request.JobResult import JobResult


class ICrawlerPlugin(object):
    __metaclass__ = ABC

    @abstractmethod
    def do_job(self, job: JobDescription) -> JobResult: raise NotImplementedError
