import os
from abc import abstractmethod
from typing import List, Tuple, TextIO
from urllib.parse import urlparse

import requests
from requests import Response

from easy_search.interfaces.crawler.communication.common.ExtendedJobDescription import ExtendedJobDescription
from easy_search.interfaces.crawler.enum.JobType import JobType
from ...exception.IncorrectJobDescriptionException import IncorrectJobDescriptionException
from ....dependency.service import hash_generator
from easy_search.interfaces.crawler.client.process.ICrawlerPlugin import ICrawlerPlugin
from easy_search.interfaces.crawler.communication.common.JobDescription import JobDescription
from easy_search.interfaces.crawler.communication.request.JobResult import JobResult
from easy_search.interfaces.crawler.index.IndexDocument import IndexDocument


class BaseFileSystemCrawlerPlugin(ICrawlerPlugin):

    def __init__(self) -> None:
        self.hash_generator = hash_generator()

    @abstractmethod
    def parse_file(self, file_handler: TextIO) -> List[IndexDocument]: raise NotImplementedError

    def do_job(self, job: ExtendedJobDescription) -> Tuple[JobResult, List[IndexDocument], List[str]]:
        path = job.target
        if not os.path.exists(path):
            raise IncorrectJobDescriptionException("Path does not exist on disk!")
        delete_list = []
        documents = []
        new_jobs = []
        if job.job_type == JobType.HARVEST:
            if not os.path.isdir(path):
                raise IncorrectJobDescriptionException("Could not perform harvest job on file!")
            for sub_path in os.listdir(path):
                full_path = os.path.join(path, sub_path)
                if os.path.isfile(full_path):
                    new_jobs = JobDescription(JobType.EXTRACT, full_path, job.plugin_type)
                elif os.path.isdir(full_path):
                    new_jobs = JobDescription(JobType.HARVEST, full_path, job.plugin_type)
        elif job.job_type == JobType.EXTRACT:
            if not os.path.isfile(path):
                raise IncorrectJobDescriptionException("Could not perform extract job on directory!")
            file_handler = open(path, encoding='utf-8')
            try:
                documents = self.parse_file(file_handler)
            finally:
                file_handler.close()

        return JobResult(job.job_id, new_jobs), documents, delete_list



