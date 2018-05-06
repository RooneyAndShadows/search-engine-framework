import urllib.parse

import jsonpickle
from jsonpickle import handlers

from core.src.crawler.client.utils.communication.exception.FailedRequestException import FailedRequestException
from core.src.crawler.client.utils.communication.http.BaseCommunicator import BaseCommunicator
from interfaces.src.base.serialize.JobTypeHandler import JobTypeHandler
from interfaces.src.crawler.client.utils.IJobCommunicator import IJobCommunicator
from interfaces.src.crawler.communication.common.JobDescription import JobDescription
from interfaces.src.crawler.communication.request.JobResult import JobResult
from interfaces.src.crawler.communication.response.JobInformation import JobInformation
import requests

from interfaces.src.crawler.enum.JobType import JobType


class JobCommunicator(IJobCommunicator, BaseCommunicator):
    def get_next_job(self) -> JobInformation:
        url = urllib.parse.urljoin(self.base_url, self.GET_NEXT_JOB_PATH)
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
        return JobInformation(job_desc)

    def finish_job(self, result: JobResult) -> None:
        url = urllib.parse.urljoin(self.base_url, self.FINISH_JOB_PATH)
        handlers.register(JobType, JobTypeHandler) 
        data = jsonpickle.encode(result, False)
        handlers.unregister(JobType)
        response = requests.post(url, data, headers=self.http_headers)
        self.validate_response(response)