from abc import ABC, abstractmethod
from typing import List, Tuple

from ...communication.common.ExtendedJobDescription import ExtendedJobDescription
from ...index.IndexDocument import IndexDocument
from ...communication.request.JobResult import JobResult


class ICrawlerPlugin(object):
    __metaclass__ = ABC

    # Returns list of new jobs + list of index documents + list of index documents to delete.
    @abstractmethod
    def do_job(self, job: ExtendedJobDescription) -> Tuple[JobResult, List[IndexDocument], List[str]]: raise NotImplementedError
