from abc import ABC, abstractmethod
from typing import List, Tuple

from easy_search.interfaces.base.job.ExtendedJobDescription import ExtendedJobDescription
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument
from easy_search.interfaces.server.job.communication import JobResult


class ICrawlerPlugin(object):
    __metaclass__ = ABC

    # Returns list of new jobs + list of index documents + list of index documents to delete.
    @abstractmethod
    def do_job(self, job: ExtendedJobDescription) -> Tuple[JobResult, List[IndexDocument], List[str]]: raise NotImplementedError
