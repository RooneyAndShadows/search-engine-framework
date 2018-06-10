from abc import abstractmethod
from typing import List, Tuple
from urllib.parse import urlparse

import requests
from requests import Response

from easy_search.interfaces.base.job.ExtendedJobDescription import ExtendedJobDescription
from easy_search.interfaces.base.enum import JobType
from easy_search.core.crawler.exception.IncorrectJobDescriptionException import IncorrectJobDescriptionException
from easy_search.core.base.dependency.service import hash_generator
from easy_search.interfaces.crawler.process import ICrawlerPlugin
from easy_search.interfaces.base.job.JobDescription import JobDescription
from easy_search.interfaces.server.job.communication import JobResult
from easy_search.interfaces.server.index.communication.common.IndexDocument import IndexDocument


class BaseHTTPCrawlerPlugin(ICrawlerPlugin):

    def __init__(self, agent: str = 'easy_search Crawler Bot') -> None:
        self.agent_string = agent
        self.hash_generator = hash_generator()

    @abstractmethod
    def parse_response(self, response: Response,
                       job_type: JobType) -> Tuple[List[IndexDocument], List[JobDescription]]: raise NotImplementedError

    def do_job(self, job: ExtendedJobDescription) -> Tuple[JobResult, List[IndexDocument], List[str]]:
        url = job.target
        delete_list = []
        documents = []
        new_jobs = []
        try:
            result = urlparse(url)
            if not (result.scheme and result.netloc and result.path):
                raise IncorrectJobDescriptionException("Invalid url given!")
        except Exception:
            raise IncorrectJobDescriptionException("Invalid url given!")
        custom_headers = {"user-agent": self.agent_string}
        response = requests.get(url, headers=custom_headers)
        if response.status_code == 404:
            delete_list.append(self.hash_generator.generate_target_hash(url))
        else:
            documents, new_jobs = self.parse_response(response, job.job_type)
        return JobResult(job.job_id, new_jobs), documents, delete_list



