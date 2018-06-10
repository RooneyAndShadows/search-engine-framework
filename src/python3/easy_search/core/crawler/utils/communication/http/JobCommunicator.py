import urllib.parse
from typing import List
from uuid import UUID

from easy_search.interfaces.base.job.ExtendedJobDescription import ExtendedJobDescription
from .....server.rest.BaseHTTPRestServer import BaseHTTPRestServer
from ..exception.FailedRequestException import FailedRequestException
from .BaseCommunicator import BaseCommunicator
from easy_search.interfaces.crawler.utils.IJobCommunicator import IJobCommunicator
from easy_search.interfaces.server.job.communication import JobResult
import requests

from easy_search.interfaces.base.enum import JobType


class JobCommunicator(IJobCommunicator, BaseCommunicator):

    def delete_job(self, job_id: UUID) -> None:
        pass

    def __init__(self, base_api_url: str, crawler_id: UUID) -> None:
        super().__init__(base_api_url, crawler_id)

    def get_next_job(self, available_plugins: List[str]) -> ExtendedJobDescription:
        url = urllib.parse.urljoin(self.base_url, BaseHTTPRestServer.JOB_FETCH_PATH)
        headers = self.http_headers
        headers['ACCEPT_PLUGINS'] = ",".join(available_plugins)
        response = requests.get(url, headers=headers)
        response_json = self.validate_response(response)
        if 'job_desc' not in response_json:
            raise FailedRequestException('Response should contain job_desc, but it does not!')
        job_desc_json = response_json['job_desc']
        if 'job_id' not in job_desc_json:
            raise FailedRequestException('Response should contain job_id, but it does not!')
        if 'job_type' not in job_desc_json:
            raise FailedRequestException('Response should contain job_type, but it does not!')
        if 'target' not in job_desc_json:
            raise FailedRequestException('Response should contain target, but it does not!')
        if 'plugin_type' not in job_desc_json:
            raise FailedRequestException('Response should contain plugin_type, but it does not!')
        job_desc = ExtendedJobDescription(job_desc_json["job_id"], JobType(job_desc_json['job_type']),
                                          job_desc_json['target'], job_desc_json['plugin_type'])
        return job_desc

    def finish_job(self, result: JobResult) -> None:
        url = urllib.parse.urljoin(self.base_url, self.FINISH_JOB_PATH)
        data = self.serialize.serialize(result)
        response = requests.post(url, data, headers=self.http_headers)
        self.validate_response(response)
