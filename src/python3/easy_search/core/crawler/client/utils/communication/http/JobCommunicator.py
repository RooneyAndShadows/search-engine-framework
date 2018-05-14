import urllib.parse
from uuid import UUID

import jsonpickle
from jsonpickle import handlers

from .....server.rest.BaseHTTPRestServer import BaseHTTPRestServer
from ..exception.FailedRequestException import FailedRequestException
from .BaseCommunicator import BaseCommunicator
from .....serialize.JobTypeHandler import JobTypeHandler
from easy_search.interfaces.crawler.client.utils.IJobCommunicator import IJobCommunicator
from easy_search.interfaces.crawler.communication.common.JobDescription import JobDescription
from easy_search.interfaces.crawler.communication.request.JobResult import JobResult
from easy_search.interfaces.crawler.communication.response.JobInformation import JobInformation
import requests

from easy_search.interfaces.crawler.enum.JobType import JobType


class JobCommunicator(IJobCommunicator, BaseCommunicator):

    def __init__(self, base_api_url: str, crawler_id: UUID) -> None:
        super().__init__(base_api_url, crawler_id)

    def get_next_job(self) -> JobDescription:
        url = urllib.parse.urljoin(self.base_url, BaseHTTPRestServer.JOB_FETCH_PATH)
        response = requests.get(url, headers=self.http_headers)
        response_json = self.validate_response(response)
        if 'job_desc' not in response_json:
            raise FailedRequestException('Response should contain job_desc, but it does not!')
        job_desc_json = response_json['job_desc']
        if 'job_type' not in job_desc_json:
            raise FailedRequestException('Response should contain job_type, but it does not!')
        if 'target' not in job_desc_json:
            raise FailedRequestException('Response should contain target, but it does not!')
        job_desc = JobDescription(JobType(job_desc_json['job_type']), job_desc_json['target'])
        return job_desc

    def finish_job(self, result: JobResult) -> None:
        url = urllib.parse.urljoin(self.base_url, self.FINISH_JOB_PATH)
        data = self.serialize.serialize(result)
        response = requests.post(url, data, headers=self.http_headers)
        self.validate_response(response)
