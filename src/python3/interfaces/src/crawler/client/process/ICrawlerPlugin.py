from abc import ABC, abstractmethod

from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.communication.response.JobInformation import JobInformation


class ICrawlerPlugin(object):
    __metaclass__ = ABC

    @abstractmethod
    def do_job(self, job: JobInformation) -> JobResult: raise NotImplementedError
